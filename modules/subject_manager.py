from database.db import get_connection

def get_subjects_hub_data(user_id: int):
    """Aggregates comprehensive data for the Subjects Hub dashboard."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT s.subject_id, s.subject_name, s.paper_name,
               COUNT(DISTINCT t.topic_id) as total_topics
        FROM subjects s
        LEFT JOIN topics t ON s.subject_id = t.subject_id
        GROUP BY s.subject_id
    """)
    subjects = cursor.fetchall()
    
    # Resource counts
    cursor.execute("""
        SELECT s.subject_id, r.resource_type, COUNT(r.resource_id)
        FROM subjects s
        JOIN topics t ON s.subject_id = t.subject_id
        JOIN resources r ON t.topic_id = r.topic_id
        GROUP BY s.subject_id, r.resource_type
    """)
    res_counts = {}
    for row in cursor.fetchall():
        sid, rtype, count = row
        if sid not in res_counts:
            res_counts[sid] = {"video": 0, "notes": 0, "pyq": 0, "practice_question": 0}
        res_counts[sid][rtype] = count
        
    # Deadlines
    cursor.execute("SELECT subject_id, recommended_completion FROM subject_deadlines WHERE user_id = ?", (user_id,))
    deadlines = {r[0]: r[1] for r in cursor.fetchall()}
    
    # Progress Calculation
    cursor.execute("""
        SELECT s.subject_id, 
               SUM(CASE WHEN p.status = 'Completed' THEN 1 ELSE 0 END) * 100.0 / NULLIF(COUNT(p.topic_id), 0) as prog
        FROM subjects s
        JOIN topics t ON s.subject_id = t.subject_id
        JOIN progress p ON t.topic_id = p.topic_id
        WHERE p.user_id = ?
        GROUP BY s.subject_id
    """, (user_id,))
    progress = {r[0]: int(r[1]) if r[1] else 0 for r in cursor.fetchall()}
    
    conn.close()
    
    result = []
    for s in subjects:
        sid = s[0]
        result.append({
            "subject_id": sid,
            "subject_name": s[1],
            "paper_name": s[2],
            "total_topics": s[3],
            "resources": res_counts.get(sid, {"video": 0, "notes": 0, "pyq": 0, "practice_question": 0}),
            "deadline": deadlines.get(sid, "Not scheduled"),
            "progress": progress.get(sid, 0)
        })
    return result

def get_subject_detail_data(user_id: int, subject_id: int):
    """Gets detailed info for a single subject."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT subject_name FROM subjects WHERE subject_id = ?", (subject_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return None
        
    name = row[0]
    
    cursor.execute("""
        SELECT t.topic_id, t.topic_name, p.status
        FROM topics t
        LEFT JOIN progress p ON t.topic_id = p.topic_id AND p.user_id = ?
        WHERE t.subject_id = ?
    """, (user_id, subject_id))
    topics = [{"topic_id": r[0], "topic_name": r[1], "status": r[2] or "Not Started"} for r in cursor.fetchall()]
    
    conn.close()
    return {"subject_id": subject_id, "subject_name": name, "topics": topics}
