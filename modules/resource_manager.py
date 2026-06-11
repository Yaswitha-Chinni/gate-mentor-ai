import os
import json
from database.queries import get_connection, get_topic_by_name

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def init_resource_tables():
    """Ensure bookmark and rating tables exist for Step 8."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookmarks (
            bookmark_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            resource_id INTEGER NOT NULL,
            UNIQUE(user_id, resource_id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ratings (
            rating_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            resource_id INTEGER NOT NULL,
            rating INTEGER NOT NULL CHECK(rating >= 1 AND rating <= 5),
            UNIQUE(user_id, resource_id)
        )
    ''')
    conn.commit()
    conn.close()

def get_all_resources() -> list:
    """Load resources from DB, fallback to JSON."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT r.resource_id, t.topic_id, t.topic_name, s.subject_name, s.paper_name, r.resource_type, r.title, r.url 
        FROM resources r
        JOIN topics t ON r.topic_id = t.topic_id
        JOIN subjects s ON t.subject_id = s.subject_id
    ''')
    rows = cursor.fetchall()
    conn.close()
    
    if rows:
        return [
            {
                "resource_id": r[0],
                "topic_id": r[1],
                "topic_name": r[2],
                "subject_name": r[3],
                "paper_name": r[4] if r[4] else "CSE",
                "resource_type": r[5],
                "title": r[6],
                "url": r[7]
            } for r in rows
        ]
        
    # Fallback to JSON
    json_path = os.path.join(BASE_DIR, "data", "sample_resources.json")
    if os.path.exists(json_path):
        with open(json_path, "r") as f:
            data = json.load(f)
            
        # Enrich JSON data with subject/topic names
        conn = get_connection()
        cursor = conn.cursor()
        enriched = []
        for r in data:
            cursor.execute('''
                SELECT t.topic_name, s.subject_name, s.paper_name
                FROM topics t 
                JOIN subjects s ON t.subject_id = s.subject_id 
                WHERE t.topic_id = ?
            ''', (r.get("topic_id"),))
            info = cursor.fetchone()
            if info:
                enriched.append({
                    "resource_id": r.get("topic_id") * 1000 + len(enriched), # fake ID for json
                    "topic_id": r.get("topic_id"),
                    "topic_name": info[0],
                    "subject_name": info[1],
                    "paper_name": info[2] if info[2] else "CSE",
                    "resource_type": r.get("resource_type"),
                    "title": r.get("title"),
                    "url": r.get("url")
                })
        conn.close()
        return enriched
    return []

def toggle_bookmark(user_id: int, resource_id: int):
    init_resource_tables()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT bookmark_id FROM bookmarks WHERE user_id = ? AND resource_id = ?", (user_id, resource_id))
    row = cursor.fetchone()
    if row:
        cursor.execute("DELETE FROM bookmarks WHERE bookmark_id = ?", (row[0],))
        action = "removed"
    else:
        cursor.execute("INSERT INTO bookmarks (user_id, resource_id) VALUES (?, ?)", (user_id, resource_id))
        action = "added"
    conn.commit()
    conn.close()
    return action

def get_user_bookmarks(user_id: int) -> set:
    init_resource_tables()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT resource_id FROM bookmarks WHERE user_id = ?", (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return set([r[0] for r in rows])

def rate_resource(user_id: int, resource_id: int, rating: int):
    init_resource_tables()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT rating_id FROM ratings WHERE user_id = ? AND resource_id = ?", (user_id, resource_id))
    row = cursor.fetchone()
    if row:
        cursor.execute("UPDATE ratings SET rating = ? WHERE rating_id = ?", (rating, row[0]))
    else:
        cursor.execute("INSERT INTO ratings (user_id, resource_id, rating) VALUES (?, ?, ?)", (user_id, resource_id, rating))
    conn.commit()
    conn.close()

def get_resource_ratings() -> dict:
    init_resource_tables()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT resource_id, AVG(rating) FROM ratings GROUP BY resource_id")
    rows = cursor.fetchall()
    conn.close()
    return {r[0]: round(r[1], 1) for r in rows}
