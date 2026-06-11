from datetime import datetime, date, timedelta
from modules.profile_manager import calculate_profile_completeness
from database.db import get_connection

def calculate_days_remaining(target_year: int) -> int:
    """Calculates days remaining until Feb 1st of the target GATE year."""
    if not target_year:
        return 0
    today = date.today()
    target_date = date(target_year, 2, 1)
    delta = target_date - today
    return max(0, delta.days)

def get_study_streak(user_id: int) -> int:
    """Calculates consecutive days of check-ins or progress updates."""
    conn = get_connection()
    cursor = conn.cursor()
    # We will use progress table completion dates as a proxy for study activity
    cursor.execute("""
        SELECT DISTINCT DATE(completion_date) 
        FROM progress 
        WHERE user_id = ? AND completion_date IS NOT NULL
        ORDER BY DATE(completion_date) DESC
    """, (user_id,))
    dates = [datetime.strptime(row[0], "%Y-%m-%d").date() for row in cursor.fetchall()]
    conn.close()
    
    if not dates:
        return 0
        
    streak = 0
    current_date = date.today()
    
    # If they haven't studied today or yesterday, streak is broken
    if dates[0] < current_date - timedelta(days=1):
        return 0
        
    expected_date = dates[0]
    for d in dates:
        if d == expected_date:
            streak += 1
            expected_date -= timedelta(days=1)
        else:
            break
            
    return streak

def get_kpi_metrics(user_id: int) -> dict:
    """Aggregates all KPIs for the modern dashboard."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Completed Subjects (where all topics are completed)
    cursor.execute("""
        SELECT COUNT(*) FROM (
            SELECT t.subject_id
            FROM topics t
            LEFT JOIN progress p ON t.topic_id = p.topic_id AND p.user_id = ?
            GROUP BY t.subject_id
            HAVING COUNT(t.topic_id) > 0 AND COUNT(t.topic_id) = SUM(CASE WHEN p.status = 'Completed' THEN 1 ELSE 0 END)
        )
    """, (user_id,))
    subjects_completed = cursor.fetchone()[0]
    
    # Completed Topics
    cursor.execute("SELECT COUNT(*) FROM progress WHERE user_id = ? AND status = 'Completed'", (user_id,))
    topics_completed = cursor.fetchone()[0]
    
    # Total available resources
    cursor.execute("SELECT resource_type, COUNT(*) FROM resources GROUP BY resource_type")
    res_counts = {r[0]: r[1] for r in cursor.fetchall()}
    
    conn.close()
    
    return {
        "subjects_completed": subjects_completed,
        "topics_completed": topics_completed,
        "videos_available": res_counts.get("video", 0),
        "notes_available": res_counts.get("notes", 0),
        "pyqs_available": res_counts.get("pyq", 0),
        "practice_sets_available": res_counts.get("practice_question", 0),
    }

def calculate_preparation_health(user_id: int, profile_completion: int, has_goal: bool, has_plan: bool) -> dict:
    score = 0
    if profile_completion == 100: score += 20
    elif profile_completion > 50: score += 10
        
    if has_goal: score += 20
    if has_plan: score += 30
        
    streak = get_study_streak(user_id)
    if streak > 7: score += 30
    elif streak > 0: score += 15
            
    status = "Needs Attention"
    if score >= 80: status = "Excellent"
    elif score >= 50: status = "Good"
        
    return {"score": score, "status": status}
