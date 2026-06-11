import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")

def migrate_resources_table():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 1. Rename old table
    cursor.execute("ALTER TABLE resources RENAME TO resources_old")
    
    # 2. Create new table without the strict CHECK constraint on resource_type
    cursor.execute('''
        CREATE TABLE resources (
            resource_id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic_id INTEGER NOT NULL,
            resource_type TEXT NOT NULL,
            title TEXT NOT NULL,
            url TEXT NOT NULL,
            FOREIGN KEY (topic_id) REFERENCES topics (topic_id) ON DELETE CASCADE
        )
    ''')
    
    # 3. Copy data
    cursor.execute('''
        INSERT INTO resources (resource_id, topic_id, resource_type, title, url)
        SELECT resource_id, topic_id, resource_type, title, url FROM resources_old
    ''')
    
    # 4. Drop old table
    cursor.execute("DROP TABLE resources_old")
    
    conn.commit()
    conn.close()
    print("Migration successful! CHECK constraint removed from resources table.")

if __name__ == "__main__":
    migrate_resources_table()
