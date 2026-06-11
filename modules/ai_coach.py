import os
from datetime import datetime, date
from database.queries import get_connection, get_progress, get_study_plan, get_goal
from modules.progress_manager import get_subject_progress, calculate_overall_completion
from modules.planner import generate_study_plan

# Optional Gemini Integration
try:
    import google.generativeai as genai
    HAS_GEMINI = True
except ImportError:
    HAS_GEMINI = False

def init_coach_tables():
    """Ensure daily check-in table exists."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS daily_checkins (
            checkin_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            checkin_date DATE NOT NULL,
            goal_completed TEXT NOT NULL,
            UNIQUE(user_id, checkin_date)
        )
    ''')
    conn.commit()
    conn.close()

def save_checkin(user_id: int, status: str):
    """Saves the daily accountability check-in."""
    init_coach_tables()
    conn = get_connection()
    cursor = conn.cursor()
    today = date.today().isoformat()
    
    cursor.execute("SELECT checkin_id FROM daily_checkins WHERE user_id = ? AND checkin_date = ?", (user_id, today))
    if cursor.fetchone():
        cursor.execute("UPDATE daily_checkins SET goal_completed = ? WHERE user_id = ? AND checkin_date = ?", (status, user_id, today))
    else:
        cursor.execute("INSERT INTO daily_checkins (user_id, checkin_date, goal_completed) VALUES (?, ?, ?)", (user_id, today, status))
    conn.commit()
    conn.close()

def get_today_checkin(user_id: int) -> str:
    """Retrieves today's check-in status if it exists."""
    init_coach_tables()
    conn = get_connection()
    cursor = conn.cursor()
    today = date.today().isoformat()
    cursor.execute("SELECT goal_completed FROM daily_checkins WHERE user_id = ? AND checkin_date = ?", (user_id, today))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None

def _get_rule_based_insights(user_id: int) -> dict:
    """Rule-based engine for AI insights if Gemini is unavailable."""
    overall = calculate_overall_completion(user_id)
    subj_prog = get_subject_progress(user_id)
    
    strong = [s for s, p in subj_prog.items() if p >= 70]
    weak = [s for s, p in subj_prog.items() if p < 40 and p > 0]
    
    if not weak and overall == 0:
        weak = ["You haven't started studying yet!"]
        
    plans = get_study_plan(user_id)
    needs_rev = [p.topic_name for p in plans if p.status == "Needs Revision"]
    pending = [p.topic_name for p in plans if p.status == "Pending" or p.status == "Not Started"]
    
    return {
        "summary": f"You have completed {overall}% of your study plan.",
        "strong": strong if strong else ["Keep studying to build your strengths!"],
        "weak": weak if weak else ["No obvious weak subjects yet."],
        "revision": needs_rev if needs_rev else ["No immediate revision needed."],
        "missed": pending[:3] if pending else ["You are fully caught up!"],
        "recommendations": [
            "Study more on weak subjects to improve your foundation.",
            "Make sure to practice PYQs for the topics you've marked as Completed.",
            "Stay consistent with your daily study hours and never skip a check-in!"
        ],
        "motivation": f"You are {overall}% through your preparation journey! Stay consistent and focus on incremental daily progress."
    }

def generate_ai_insights(user_id: int) -> dict:
    """Generates AI insights via Gemini API or falls back to rule-based logic."""
    api_key = os.environ.get("GOOGLE_API_KEY") or None
    
    if HAS_GEMINI and api_key:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            overall = calculate_overall_completion(user_id)
            subj_prog = get_subject_progress(user_id)
            
            prompt = f"""
            You are an expert AI Study Coach for a student preparing for the GATE exam.
            Here is their current progress data:
            - Overall Completion: {overall}%
            - Subject Progress: {subj_prog}
            
            Provide a short, highly motivating analysis with these exact Markdown headers:
            ### Progress Summary
            ### Strong Subjects
            ### Weak Subjects
            ### Recommendations
            ### Motivation
            """
            
            response = model.generate_content(prompt)
            return {"type": "ai_raw", "content": response.text}
            
        except Exception as e:
            print(f"Gemini API Error: {e}")
            return {"type": "rule_based", "content": _get_rule_based_insights(user_id)}
    else:
        # Fallback
        return {"type": "rule_based", "content": _get_rule_based_insights(user_id)}

def generate_regenerated_plan(user_id: int) -> dict:
    """Regenerates the plan by recalculating from today's date."""
    # In a full production app, this would preserve completed topics.
    # For MVP, we invoke the planner with the 'Serious' intensity to simulate an adaptive push.
    return generate_study_plan(user_id, "Serious")
