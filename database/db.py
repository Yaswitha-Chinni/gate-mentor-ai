import sqlite3
import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database.db")

def get_connection():
    """Create and return a database connection with foreign key support."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def initialize_database():
    """Create all tables and insert default data if needed."""
    conn = get_connection()
    cursor = conn.cursor()

    # Users Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            mobile TEXT,
            gender TEXT,
            college_name TEXT,
            college_website TEXT,
            degree TEXT,
            current_branch TEXT,
            current_year TEXT,
            current_semester TEXT,
            graduation_year INTEGER,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Gate Goals Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS gate_goals (
            goal_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            target_gate_year INTEGER NOT NULL,
            target_papers TEXT NOT NULL,
            target_rank INTEGER,
            target_score INTEGER,
            attempt_type TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE
        )
    ''')

    # Subjects Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS subjects (
            subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject_name TEXT UNIQUE NOT NULL,
            weightage INTEGER
        )
    ''')

    # Topics Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS topics (
            topic_id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject_id INTEGER NOT NULL,
            topic_name TEXT NOT NULL,
            estimated_hours INTEGER,
            FOREIGN KEY (subject_id) REFERENCES subjects (subject_id) ON DELETE CASCADE
        )
    ''')

    # Study Plans Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS study_plans (
            plan_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            month_number INTEGER NOT NULL,
            subject_name TEXT NOT NULL,
            topic_name TEXT NOT NULL,
            planned_hours INTEGER,
            status TEXT DEFAULT 'Pending',
            FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE
        )
    ''')

    # Progress Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS progress (
            progress_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            topic_id INTEGER NOT NULL,
            status TEXT CHECK(status IN ('Completed', 'In Progress', 'Pending', 'Needs Revision')) DEFAULT 'Pending',
            completion_date DATETIME,
            study_hours INTEGER,
            FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE,
            FOREIGN KEY (topic_id) REFERENCES topics (topic_id) ON DELETE CASCADE
        )
    ''')

    # Resources Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS resources (
            resource_id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic_id INTEGER NOT NULL,
            resource_type TEXT NOT NULL,
            title TEXT NOT NULL,
            url TEXT NOT NULL,
            FOREIGN KEY (topic_id) REFERENCES topics (topic_id) ON DELETE CASCADE
        )
    ''')

    conn.commit()
    
    # Try adding new columns to existing tables
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN telegram_id TEXT")
    except sqlite3.OperationalError:
        pass
        
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN whatsapp_number TEXT")
    except sqlite3.OperationalError:
        pass
        
    try:
        cursor.execute("ALTER TABLE subjects ADD COLUMN paper_name TEXT DEFAULT 'CSE'")
    except sqlite3.OperationalError:
        pass
        
    # Future Ready Tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS academic_calendars (
            calendar_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            calendar_url TEXT,
            semester_dates TEXT,
            mid_exams TEXT,
            end_exams TEXT,
            holidays TEXT,
            FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS subject_deadlines (
            deadline_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            subject_id INTEGER NOT NULL,
            recommended_completion DATE,
            revision_date DATE,
            pyq_deadline DATE,
            FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE,
            FOREIGN KEY (subject_id) REFERENCES subjects (subject_id) ON DELETE CASCADE
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rank_predictions (
            prediction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            predicted_rank INTEGER NOT NULL,
            confidence REAL,
            prediction_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS knowledge_chunks (
            chunk_id INTEGER PRIMARY KEY AUTOINCREMENT,
            document_id TEXT NOT NULL,
            content TEXT NOT NULL,
            embedding TEXT,
            metadata TEXT
        )
    ''')
    
    conn.commit()

    # Load default data
    _load_syllabus(cursor)

    conn.commit()
    conn.close()

def _load_syllabus(cursor):
    """Internal function to load syllabus JSON if subjects are empty."""
    cursor.execute("SELECT COUNT(*) FROM subjects")
    if cursor.fetchone()[0] == 0:
        syllabus_path = os.path.join(BASE_DIR, "data", "gate_cse_syllabus.json")
        if os.path.exists(syllabus_path):
            with open(syllabus_path, "r") as f:
                syllabus = json.load(f)
            
            for subj_name, topics in syllabus.items():
                cursor.execute("INSERT INTO subjects (subject_name) VALUES (?)", (subj_name,))
                subject_id = cursor.lastrowid
                for topic in topics:
                    cursor.execute("INSERT INTO topics (subject_id, topic_name) VALUES (?, ?)", (subject_id, topic))

if __name__ == "__main__":
    initialize_database()
    print("Database initialization complete.")
