import sqlite3
import urllib.parse

def populate_resources():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Check if already populated to avoid duplicates
    cursor.execute("SELECT count(*) FROM resources")
    if cursor.fetchone()[0] > 0:
        print("Resources already populated. Clearing existing resources to regenerate...")
        cursor.execute("DELETE FROM resources")
        
    cursor.execute("SELECT t.topic_id, t.topic_name, s.subject_name FROM topics t JOIN subjects s ON t.subject_id = s.subject_id")
    topics = cursor.fetchall()
    
    resources_to_insert = []
    
    for topic_id, topic_name, subject_name in topics:
        # URL encode the topic name for search queries
        query = urllib.parse.quote(f"GATE CSE {subject_name} {topic_name}")
        gfg_query = urllib.parse.quote(f"{topic_name}")
        go_query = urllib.parse.quote(f"{topic_name}")
        
        # 1. Video Playlist (YouTube Search)
        resources_to_insert.append((
            topic_id,
            "video",
            f"Video Lectures: {topic_name}",
            f"https://www.youtube.com/results?search_query={query}"
        ))
        
        # 2. Handwritten Notes (GeeksforGeeks Search)
        resources_to_insert.append((
            topic_id,
            "notes",
            f"Complete Notes: {topic_name}",
            f"https://www.geeksforgeeks.org/search/?q={gfg_query}"
        ))
        
        # 3. PYQs (GateOverflow Search)
        resources_to_insert.append((
            topic_id,
            "pyq",
            f"Previous Year Questions: {topic_name}",
            f"https://gateoverflow.in/questions?q={go_query}"
        ))
        
        # 4. Practice Set (Sanfoundry or general search)
        resources_to_insert.append((
            topic_id,
            "practice_question",
            f"Practice Set: {topic_name}",
            f"https://www.google.com/search?q={query}+MCQ+Practice+Questions"
        ))
        
    # Insert in batch
    cursor.executemany('''
        INSERT INTO resources (topic_id, resource_type, title, url)
        VALUES (?, ?, ?, ?)
    ''', resources_to_insert)
    
    conn.commit()
    print(f"Successfully populated {len(resources_to_insert)} resources across {len(topics)} topics!")
    conn.close()

if __name__ == "__main__":
    populate_resources()
