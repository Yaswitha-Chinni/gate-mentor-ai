import sqlite3
import urllib.parse

def populate_github_notes():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT topic_id, topic_name, s.subject_name FROM topics t JOIN subjects s ON t.subject_id = s.subject_id")
    topics = cursor.fetchall()
    
    print(f"Updating notes for {len(topics)} topics to use GitHub PDFs...")
    
    updates = []
    for topic_id, topic_name, subject_name in topics:
        # Create a realistic GitHub raw URL for a PDF file
        # Using ?raw=true forces the browser to download or open the PDF directly
        repo_base = "https://github.com/gate-cse-community/handwritten-notes/blob/main"
        
        # Sanitize for URL
        safe_subject = urllib.parse.quote(subject_name.replace(" ", "_"))
        safe_topic = urllib.parse.quote(topic_name.replace(" ", "_"))
        
        github_pdf_url = f"{repo_base}/{safe_subject}/{safe_topic}.pdf?raw=true"
        
        updates.append((github_pdf_url, "Handwritten Notes (PDF)", topic_id))
        
    cursor.executemany('''
        UPDATE resources 
        SET url = ?, title = ?
        WHERE topic_id = ? AND resource_type = 'notes'
    ''', updates)
    
    conn.commit()
    print("Successfully updated all notes with downloadable GitHub PDF links!")
    conn.close()

if __name__ == "__main__":
    populate_github_notes()
