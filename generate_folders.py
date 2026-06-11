import os
import sqlite3
import shutil
from database.db import initialize_database

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")
DOWNLOADS_DIR = os.path.join(BASE_DIR, "frontend", "downloads", "GATE-CS")

# Dummy source files
DUMMY_PDF = os.path.join(BASE_DIR, "frontend", "downloads", "gate_cse_notes.pdf")
DUMMY_PNG = os.path.join(BASE_DIR, "frontend", "assets", "logo.png") # just use anything if needed, or create an empty file

def create_empty_pdf(path):
    if os.path.exists(DUMMY_PDF):
        shutil.copy(DUMMY_PDF, path)
    else:
        with open(path, "w") as f:
            f.write("Dummy PDF content")

def create_empty_png(path):
    with open(path, "wb") as f:
        # 1x1 transparent PNG
        f.write(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82')

def create_empty_json(path):
    with open(path, "w") as f:
        f.write("[]")

def reset_db_and_generate():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 1. Clear old data
    cursor.execute("PRAGMA foreign_keys=OFF;")
    cursor.execute("DELETE FROM resources;")
    cursor.execute("DELETE FROM progress;")
    cursor.execute("DELETE FROM topics;")
    cursor.execute("DELETE FROM subjects;")
    conn.commit()
    cursor.execute("PRAGMA foreign_keys=ON;")
    
    # 2. Reload syllabus
    initialize_database()
    
    # 3. Create folders and resources
    cursor.execute("SELECT t.topic_id, t.topic_name, s.subject_name FROM topics t JOIN subjects s ON t.subject_id = s.subject_id")
    topics = cursor.fetchall()
    
    files_to_create = [
        ("Notes", "notes", "Notes.pdf", create_empty_pdf),
        ("Handwritten Notes", "handwritten_notes", "Handwritten_Notes.pdf", create_empty_pdf),
        ("PYQs", "pyq", "PYQs.pdf", create_empty_pdf),
        ("Formula Sheet", "formula_sheet", "Formula_Sheet.pdf", create_empty_pdf),
        ("Quiz", "quiz", "Quiz.json", create_empty_json),
        ("Flashcards", "flashcards", "Flashcards.json", create_empty_json),
        ("Mindmap", "mindmap", "Mindmap.png", create_empty_png),
        ("Revision Notes", "revision_notes", "Revision_Notes.pdf", create_empty_pdf),
    ]
    
    for topic_id, topic_name, subject_name in topics:
        # Build folder path
        parts = topic_name.split(" - ")
        folder_path = os.path.join(DOWNLOADS_DIR, subject_name, *parts)
        os.makedirs(folder_path, exist_ok=True)
        
        # Build relative URL base
        url_parts = [subject_name] + parts
        # URL encode spaces? The web server will handle it if we use standard URL rules, but let's just replace spaces with %20 in DB if needed, or rely on frontend.
        # Actually it's better to URL encode the path
        import urllib.parse
        base_url = "/assets/downloads/GATE-CS/" + "/".join(urllib.parse.quote(p) for p in url_parts) + "/"
        
        for title, r_type, filename, create_func in files_to_create:
            file_path = os.path.join(folder_path, filename)
            create_func(file_path)
            
            # Insert into DB
            url = base_url + filename
            cursor.execute('''
                INSERT INTO resources (topic_id, resource_type, title, url)
                VALUES (?, ?, ?, ?)
            ''', (topic_id, r_type, f"{topic_name} - {title}", url))
            
    conn.commit()
    conn.close()
    print("Folders and resources generated successfully!")

if __name__ == "__main__":
    reset_db_and_generate()
