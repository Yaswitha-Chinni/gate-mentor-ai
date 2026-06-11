import streamlit as st
from utils.gemini_helper import get_gemini_model
from utils.quiz_utils import generate_quiz, parse_quiz


def render():
    st.title("📝 Quiz Generator")
    st.markdown("Test your knowledge with an AI-generated multiple choice quiz based on your materials.")

    source_option = st.radio("Select Source", ["Use Uploaded Documents", "Paste Text"])
    text_to_process = ""

    if source_option == "Use Uploaded Documents":
        if "documents" in st.session_state and len(st.session_state["documents"]) > 0:
            doc_names = [doc["name"] for doc in st.session_state["documents"]]
            selected_doc_name = st.selectbox("Select a document", doc_names)

            for doc in st.session_state["documents"]:
                if doc["name"] == selected_doc_name:
                    text_to_process = doc["text"]
                    break
        else:
            st.info("No documents uploaded yet. Go to the PDF Summarizer or Lecture Notes page to upload a file.")
    else:
        text_to_process = st.text_area("Paste text here to generate a quiz", height=200)

    if st.button("Generate Quiz"):
        if text_to_process:
            with st.spinner("Generating 10 MCQs using Gemini..."):
                try:
                    llm = get_gemini_model()
                    # Trim to avoid exceeding context for simple generation
                    text_to_process = text_to_process[:15000]

                    quiz_raw = generate_quiz(text_to_process, llm)
                    questions = parse_quiz(quiz_raw)

                    if questions:
                        st.success(f"Successfully generated {len(questions)} questions!")
                        st.session_state["current_quiz"] = questions
                        # Reset answers
                        for i in range(len(questions)):
                            st.session_state[f"q_{i}"] = None
                    else:
                        st.error("Failed to parse the quiz. Please try again.")

                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Please provide some text to generate a quiz.")

    # Interactive Quiz UI
    if "current_quiz" in st.session_state and st.session_state["current_quiz"]:
        st.markdown("### Interactive Quiz")

        questions = st.session_state["current_quiz"]

        with st.form("quiz_form"):
            for i, q in enumerate(questions):
                st.markdown(f"**Q{i+1}: {q['question']}**")
                # Create radio buttons for options
                st.radio(
                    "Select your answer:", 
                    q['options'], 
                    key=f"user_ans_{i}",
                    index=None
                )
                st.markdown("---")

            submitted = st.form_submit_button("Submit Answers")

            if submitted:
                score = 0
                for i, q in enumerate(questions):
                    user_ans = st.session_state.get(f"user_ans_{i}")
                    correct_ans = q['answer']

                    # Check if the user answer contains the correct answer letter or matches
                    # Often the user_ans looks like "A) Option text" and correct_ans is "A"
                    if user_ans and user_ans.startswith(correct_ans):
                        score += 1

                st.session_state["quiz_score"] = score
                st.session_state["quiz_submitted"] = True

    # Show Results outside the form so it persists properly
    if st.session_state.get("quiz_submitted", False):
        questions = st.session_state["current_quiz"]
        score = st.session_state.get("quiz_score", 0)

        st.markdown(f"### 🎉 Your Score: {score} / {len(questions)}")

        with st.expander("Review Answers"):
            for i, q in enumerate(questions):
                user_ans = st.session_state.get(f"user_ans_{i}")
                correct_ans = q['answer']
                is_correct = user_ans and user_ans.startswith(correct_ans)

                st.markdown(f"**Q{i+1}: {q['question']}**")
                st.write(f"Your Answer: {user_ans if user_ans else 'No answer selected'}")
                if is_correct:
                    st.success(f"Correct! (Answer: {correct_ans})")
                else:
                    st.error(f"Incorrect. The correct answer was: {correct_ans}")
                st.markdown("---")
