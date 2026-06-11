import sqlite3

def update_arrays_resources():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Update notes for Arrays
    cursor.execute('''
        UPDATE resources 
        SET url = '/assets/downloads/arrays_handwritten_notes.pdf' 
        WHERE topic_id IN (SELECT topic_id FROM topics WHERE topic_name = 'Arrays') 
        AND resource_type = 'notes'
    ''')
    
    # Update practice for Arrays
    cursor.execute('''
        UPDATE resources 
        SET url = '/assets/downloads/arrays_mcq_practice.pdf' 
        WHERE topic_id IN (SELECT topic_id FROM topics WHERE topic_name = 'Arrays') 
        AND resource_type = 'practice_question'
    ''')
    
    conn.commit()
    print("Database updated for Arrays.")
    conn.close()

if __name__ == "__main__":
    update_arrays_resources()
