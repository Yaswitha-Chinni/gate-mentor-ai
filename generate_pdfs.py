import os
from fpdf import FPDF
from PIL import Image

def images_to_pdf(image_paths, output_pdf_path):
    pdf = FPDF()
    for image_path in image_paths:
        # Open image to get dimensions and convert to JPG for fpdf compatibility
        img = Image.open(image_path)
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
            
        temp_jpg = image_path + ".jpg"
        img.save(temp_jpg, "JPEG")
        
        pdf.add_page()
        pdf.image(temp_jpg, x=0, y=0, w=210, h=297)
        
        # Cleanup
        if os.path.exists(temp_jpg):
            os.remove(temp_jpg)
            
    pdf.output(output_pdf_path)
    print(f"Generated {output_pdf_path}")

if __name__ == "__main__":
    downloads_dir = os.path.join("frontend", "downloads")
    os.makedirs(downloads_dir, exist_ok=True)
    
    brain_dir = r"C:\Users\yaswi\.gemini\antigravity\brain\4a019342-c9dd-4e4c-a496-f28261e4bb4e"
    
    notes_img = os.path.join(brain_dir, "arrays_notes_page1_1781078205344.png")
    mcq1 = os.path.join(brain_dir, "arrays_mcq_page1_1781078240148.png")
    mcq2 = os.path.join(brain_dir, "arrays_mcq_page2_1781078277723.png")
    mcq3 = os.path.join(brain_dir, "arrays_mcq_page3_1781078299744.png")
    
    out_notes = os.path.join(downloads_dir, "arrays_handwritten_notes.pdf")
    out_mcqs = os.path.join(downloads_dir, "arrays_mcq_practice.pdf")
    
    images_to_pdf([notes_img], out_notes)
    images_to_pdf([mcq1, mcq2, mcq3], out_mcqs)
