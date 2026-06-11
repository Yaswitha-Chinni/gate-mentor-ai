import pypdf
import io

def extract_text_from_pdf(uploaded_file):
    """
    Extracts text from a Streamlit UploadedFile (PDF).
    """
    try:
        pdf_reader = pypdf.PdfReader(io.BytesIO(uploaded_file.read()))
        text = ""
        for page in pdf_reader.pages:
            extracted_text = page.extract_text()
            if extracted_text:
                text += extracted_text + "\n"
        return text
    except Exception as e:
        raise Exception(f"Error extracting text from PDF: {str(e)}")

def generate_pdf_summary(text, llm):
    """
    Generates a concise summary from extracted text.
    """
    prompt = f"""
    You are an expert educational assistant. Please summarize the following text comprehensively but concisely.
    Extract the key points and important concepts.

    Text:
    {text}
    """
    response = llm.invoke(prompt)
    return response.content
