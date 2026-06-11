import sqlite3
import urllib.parse

def fix_links():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT topic_id, topic_name FROM topics")
    topics = cursor.fetchall()
    
    notes_updates = []
    practice_updates = []
    
    for topic_id, topic_name in topics:
        safe_topic = urllib.parse.quote(topic_name)
        
        # Broaden notes search to ensure results
        notes_search_url = f"https://www.google.com/search?q={safe_topic}+GATE+CSE+handwritten+notes+pdf+download"
        notes_updates.append((notes_search_url, topic_id))
        
        # Change practice search from Sanfoundry to Google search for MCQs to avoid Cloudflare blocks
        practice_url = f"https://www.google.com/search?q={safe_topic}+MCQ+practice+questions+pdf"
        practice_updates.append((practice_url, topic_id))
        
    cursor.executemany('''
        UPDATE resources 
        SET url = ? 
        WHERE topic_id = ? AND resource_type = 'notes'
    ''', notes_updates)
    
    cursor.executemany('''
        UPDATE resources 
        SET url = ? 
        WHERE topic_id = ? AND resource_type = 'practice_question'
    ''', practice_updates)
    
    conn.commit()
    print("Successfully fixed Notes and Practice Links!")
    conn.close()

if __name__ == "__main__":
    fix_links()
