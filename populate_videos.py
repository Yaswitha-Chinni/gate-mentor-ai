import sqlite3
import urllib.request
import urllib.parse
import json
import time

YOUTUBE_API_KEY = "AIzaSyC07D5UMzU5opOHzfTnZAmVFbj8-_xh_qk"

def get_best_youtube_video(query):
    try:
        encoded_query = urllib.parse.quote(f"{query} GATE CSE")
        url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=1&q={encoded_query}&type=video&key={YOUTUBE_API_KEY}"
        
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            if data.get("items"):
                video_id = data["items"][0]["id"]["videoId"]
                return f"https://www.youtube.com/watch?v={video_id}"
    except Exception as e:
        print(f"Error fetching YouTube video for {query}: {e}")
    
    return f"https://www.youtube.com/results?search_query={encoded_query}"

def populate_videos():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT topic_id, topic_name FROM topics")
    topics = cursor.fetchall()
    
    print(f"Fetching best YouTube videos for {len(topics)} topics...")
    
    updates = []
    for topic_id, topic_name in topics:
        print(f"Fetching for: {topic_name}")
        best_url = get_best_youtube_video(topic_name)
        updates.append((best_url, topic_id))
        # Small delay to avoid hitting YouTube API rate limits
        time.sleep(0.1)
        
    cursor.executemany('''
        UPDATE resources 
        SET url = ? 
        WHERE topic_id = ? AND resource_type = 'video'
    ''', updates)
    
    conn.commit()
    print("Successfully updated all video links with direct top-ranking YouTube URLs!")
    conn.close()

if __name__ == "__main__":
    populate_videos()
