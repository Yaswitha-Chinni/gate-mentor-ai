import json
from database.db import get_connection

def save_calendar_data(user_id: int, url: str, data: dict):
    """Saves the extracted academic calendar data into the database."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Safely handle JSON dumps
    sem_dates = json.dumps(data.get("semester_dates", {}))
    mid_exams = json.dumps(data.get("mid_exams", {}))
    end_exams = json.dumps(data.get("end_exams", {}))
    holidays = json.dumps(data.get("holidays", []))
    
    cursor.execute("SELECT calendar_id FROM academic_calendars WHERE user_id = ?", (user_id,))
    if cursor.fetchone():
        cursor.execute("""
            UPDATE academic_calendars 
            SET calendar_url = ?, semester_dates = ?, mid_exams = ?, end_exams = ?, holidays = ? 
            WHERE user_id = ?
        """, (url, sem_dates, mid_exams, end_exams, holidays, user_id))
    else:
        cursor.execute("""
            INSERT INTO academic_calendars (user_id, calendar_url, semester_dates, mid_exams, end_exams, holidays)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, url, sem_dates, mid_exams, end_exams, holidays))
    conn.commit()
    conn.close()
    return {"success": True, "message": "Academic Calendar integrated successfully."}

def get_calendar_data(user_id: int):
    """Retrieves the academic calendar for the user."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT calendar_url, semester_dates, mid_exams, end_exams, holidays FROM academic_calendars WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {
            "calendar_url": row[0],
            "semester_dates": json.loads(row[1]) if row[1] else {},
            "mid_exams": json.loads(row[2]) if row[2] else {},
            "end_exams": json.loads(row[3]) if row[3] else {},
            "holidays": json.loads(row[4]) if row[4] else []
        }
    return None

def simulate_extraction(filename: str):
    """Simulates AI-based PDF extraction for the MVP."""
    return {
        "semester_dates": {"start": "2024-08-01", "end": "2024-12-15"},
        "mid_exams": {"start": "2024-10-10", "end": "2024-10-15"},
        "end_exams": {"start": "2024-12-01", "end": "2024-12-10"},
        "holidays": ["2024-08-15", "2024-10-02", "2024-10-31", "2024-12-25"]
    }
