def generate_quiz(text, llm):
    """
    Generates a 10-question MCQ quiz from the provided text using Gemini.
    """
    prompt = f"""
    You are an expert quiz generator. Based on the following text, create exactly 10 Multiple Choice Questions (MCQs).
    For each question, provide 4 options and clearly indicate the correct answer.
    
    Format the output strictly as follows:
    Q1: [Question text]
    A) [Option A]
    B) [Option B]
    C) [Option C]
    D) [Option D]
    Answer: [Correct Option Letter]
    
    ...and so on up to Q10.

    Text:
    {text}
    """
    response = llm.invoke(prompt)
    return response.content

def parse_quiz(quiz_text):
    """
    Parses the generated quiz text into a structured format (list of dicts).
    """
    questions = []
    blocks = quiz_text.split("Q")[1:]  # split by Q1:, Q2:, etc.
    
    for block in blocks:
        try:
            lines = block.strip().split("\n")
            # Extract question number and text
            q_line_parts = lines[0].split(":", 1)
            q_text = q_line_parts[1].strip()
            
            options = []
            answer = ""
            for line in lines[1:]:
                line = line.strip()
                if line.startswith("A)") or line.startswith("B)") or line.startswith("C)") or line.startswith("D)"):
                    options.append(line)
                elif line.startswith("Answer:"):
                    answer = line.split(":", 1)[1].strip()
            
            if q_text and len(options) == 4 and answer:
                questions.append({
                    "question": q_text,
                    "options": options,
                    "answer": answer
                })
        except Exception:
            continue
            
    return questions
