import sqlite3
import urllib.parse

def populate_fixes():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Bypass CHECK constraint by recreating the table
    cursor.execute("PRAGMA foreign_keys=off;")
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS resources_new (
            resource_id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic_id INTEGER NOT NULL,
            resource_type TEXT CHECK(resource_type IN ('video', 'notes', 'pyq', 'practice_question', 'book')) NOT NULL,
            title TEXT NOT NULL,
            url TEXT NOT NULL,
            FOREIGN KEY (topic_id) REFERENCES topics (topic_id) ON DELETE CASCADE
        )
    ''')
    
    cursor.execute("INSERT INTO resources_new SELECT * FROM resources")
    cursor.execute("DROP TABLE resources")
    cursor.execute("ALTER TABLE resources_new RENAME TO resources")
    cursor.execute("PRAGMA foreign_keys=on;")
    
    cursor.execute("SELECT topic_id, topic_name, s.subject_name, s.subject_id FROM topics t JOIN subjects s ON t.subject_id = s.subject_id")
    topics = cursor.fetchall()
    
    print(f"Applying fixes to resources...")
    
    added_books = set()
    book_recommendations = {
        "Programming & Data Structures": ("Data Structures and Algorithms in C by Reema Thareja", "https://www.google.com/search?q=Data+Structures+and+Algorithms+in+C+by+Reema+Thareja+pdf"),
        "Algorithms": ("Introduction to Algorithms by Cormen (CLRS)", "https://www.google.com/search?q=Introduction+to+Algorithms+by+Cormen+CLRS+pdf"),
        "Operating Systems": ("Operating System Concepts by Galvin", "https://www.google.com/search?q=Operating+System+Concepts+by+Galvin+pdf"),
        "DBMS": ("Database System Concepts by Korth", "https://www.google.com/search?q=Database+System+Concepts+by+Korth+pdf"),
        "Computer Networks": ("Computer Networking: A Top-Down Approach by Kurose & Ross", "https://www.google.com/search?q=Computer+Networking+Top+Down+Approach+Kurose+pdf"),
        "Theory of Computation": ("Introduction to Automata Theory by Ullman", "https://www.google.com/search?q=Introduction+to+Automata+Theory+Ullman+pdf"),
        "Compiler Design": ("Compilers: Principles, Techniques, and Tools by Ullman (Dragon Book)", "https://www.google.com/search?q=Compilers+Dragon+Book+Ullman+pdf"),
        "Digital Logic": ("Digital Design by M. Morris Mano", "https://www.google.com/search?q=Digital+Design+Morris+Mano+pdf"),
        "Computer Organization": ("Computer Organization and Architecture by William Stallings", "https://www.google.com/search?q=Computer+Organization+William+Stallings+pdf"),
        "Engineering Mathematics": ("Higher Engineering Mathematics by B.S. Grewal", "https://www.google.com/search?q=Higher+Engineering+Mathematics+BS+Grewal+pdf"),
        "Discrete Mathematics": ("Discrete Mathematics and Its Applications by Kenneth Rosen", "https://www.google.com/search?q=Discrete+Mathematics+Kenneth+Rosen+pdf")
    }

    notes_updates = []
    practice_updates = []
    books_inserts = []
    
    for topic_id, topic_name, subject_name, subject_id in topics:
        safe_topic = urllib.parse.quote(topic_name)
        github_search_url = f"https://www.google.com/search?q=site:github.com+GATE+CSE+{safe_topic}+notes+filetype:pdf"
        notes_updates.append((github_search_url, topic_id))
        
        sanfoundry_url = f"https://www.sanfoundry.com/search/?q={safe_topic}"
        practice_updates.append((sanfoundry_url, topic_id))
        
        if subject_name not in added_books and subject_name in book_recommendations:
            book_title, book_url = book_recommendations[subject_name]
            books_inserts.append((topic_id, 'book', f"Standard Textbook: {book_title}", book_url))
            added_books.add(subject_name)
            
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
    
    cursor.executemany('''
        INSERT INTO resources (topic_id, resource_type, title, url)
        VALUES (?, ?, ?, ?)
    ''', books_inserts)
    
    conn.commit()
    print("Successfully fixed Notes, Practice Links, and inserted Standard Reference Books!")
    conn.close()

if __name__ == "__main__":
    populate_fixes()
