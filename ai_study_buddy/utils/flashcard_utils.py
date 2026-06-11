def generate_flashcards(text, llm):
    """
    Generates Question and Answer flashcards from the provided text using Gemini.
    """
    prompt = f"""
    You are an expert study aid creator. Based on the following text, create a set of flashcards covering the key concepts.
    Generate around 5 to 10 flashcards depending on the text length.
    
    Format the output strictly as follows:
    Q: [Question]
    A: [Answer]
    
    Q: [Question]
    A: [Answer]

    Text:
    {text}
    """
    response = llm.invoke(prompt)
    return response.content

def parse_flashcards(flashcards_text):
    """
    Parses the generated flashcards text into a structured format.
    """
    flashcards = []
    lines = flashcards_text.strip().split("\n")
    
    current_q = None
    current_a = None
    
    for line in lines:
        line = line.strip()
        if line.startswith("Q:"):
            current_q = line[2:].strip()
        elif line.startswith("A:"):
            current_a = line[2:].strip()
            if current_q and current_a:
                flashcards.append({"question": current_q, "answer": current_a})
                current_q = None
                current_a = None
                
    return flashcards
