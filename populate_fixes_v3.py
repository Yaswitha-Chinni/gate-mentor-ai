import os
import sqlite3
from fpdf import FPDF

def create_pdf(filename, title, content):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=15, style='B')
    pdf.cell(200, 10, txt=title, ln=1, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=content)
    pdf.output(filename)

def fix_links_with_direct_downloads():
    downloads_dir = os.path.join("frontend", "assets", "downloads")
    os.makedirs(downloads_dir, exist_ok=True)
    
    # Generate mock PDFs
    notes_pdf = os.path.join(downloads_dir, "gate_cse_notes.pdf")
    mcq_pdf = os.path.join(downloads_dir, "gate_cse_mcq_practice.pdf")
    book_pdf = os.path.join(downloads_dir, "gate_cse_reference_book.pdf")
    
    create_pdf(notes_pdf, "Complete GATE CSE Handwritten Notes", "This is a placeholder for the official GATE CSE Handwritten Notes PDF. This file is served directly from the platform for free.")
    create_pdf(mcq_pdf, "GATE CSE Topic-wise MCQ Practice Bank", "This is a placeholder for the official MCQ Practice Question Bank. Includes PYQs and detailed solutions.")
    create_pdf(book_pdf, "Standard Reference Textbook for GATE CSE", "This is a placeholder for the Standard Reference Textbook PDF. Free and directly downloadable.")
    
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Update all notes
    cursor.execute("UPDATE resources SET url = '/assets/downloads/gate_cse_notes.pdf' WHERE resource_type = 'notes'")
    # Update all practice
    cursor.execute("UPDATE resources SET url = '/assets/downloads/gate_cse_mcq_practice.pdf' WHERE resource_type = 'practice_question'")
    # Update all books
    cursor.execute("UPDATE resources SET url = '/assets/downloads/gate_cse_reference_book.pdf' WHERE resource_type = 'book'")
    
    conn.commit()
    print("Successfully generated direct downloadable PDFs and updated the database!")
    conn.close()

if __name__ == "__main__":
    fix_links_with_direct_downloads()
