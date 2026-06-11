import sqlite3
import time
from duckduckgo_search import DDGS

def get_first_result(query, site_filter=None):
    if site_filter:
        query = f"{query} site:{site_filter}"
    try:
        results = DDGS().text(query, max_results=1)
        if results:
            return results[0]['href']
    except Exception as e:
        print(f"Error fetching {query}: {e}")
    return None

def populate_resources():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Clear existing generic links
    cursor.execute("DELETE FROM resources")
    
    cursor.execute("SELECT t.topic_id, t.topic_name, s.subject_name FROM topics t JOIN subjects s ON t.subject_id = s.subject_id")
    topics = cursor.fetchall()
    
    resources_to_insert = []
    
    print("Fetching direct URLs. This will take a moment to avoid rate limits...")
    for topic_id, topic_name, subject_name in topics:
        print(f"Fetching resources for: {topic_name}")
        
        # 1. Video (YouTube)
        video_url = get_first_result(f"GATE CSE {subject_name} {topic_name}", "youtube.com")
        if not video_url: video_url = f"https://www.youtube.com/results?search_query=GATE+CSE+{topic_name.replace(' ', '+')}"
        resources_to_insert.append((topic_id, "video", f"Video Lectures: {topic_name}", video_url))
        time.sleep(1.5)
        
        # 2. Notes (GeeksforGeeks)
        notes_url = get_first_result(f"{topic_name} GATE CSE", "geeksforgeeks.org")
        if not notes_url: notes_url = f"https://www.geeksforgeeks.org/search/?q={topic_name.replace(' ', '+')}"
        resources_to_insert.append((topic_id, "notes", f"Complete Notes: {topic_name}", notes_url))
        time.sleep(1.5)
        
        # 3. PYQs (GateOverflow)
        pyq_url = get_first_result(f"{topic_name} GATE questions", "gateoverflow.in")
        if not pyq_url: pyq_url = f"https://gateoverflow.in/questions?q={topic_name.replace(' ', '+')}"
        resources_to_insert.append((topic_id, "pyq", f"Previous Year Questions: {topic_name}", pyq_url))
        time.sleep(1.5)
        
        # 4. Practice Set (Sanfoundry or general)
        practice_url = get_first_result(f"{topic_name} MCQ practice questions", "sanfoundry.com")
        if not practice_url: practice_url = get_first_result(f"{topic_name} MCQ practice questions")
        if not practice_url: practice_url = f"https://www.google.com/search?q={topic_name.replace(' ', '+')}+MCQ"
        resources_to_insert.append((topic_id, "practice_question", f"Practice Set: {topic_name}", practice_url))
        time.sleep(1.5)
        
    cursor.executemany('''
        INSERT INTO resources (topic_id, resource_type, title, url)
        VALUES (?, ?, ?, ?)
    ''', resources_to_insert)
    
    conn.commit()
    print(f"Successfully populated {len(resources_to_insert)} DIRECT resources!")
    conn.close()

if __name__ == "__main__":
    populate_resources()
