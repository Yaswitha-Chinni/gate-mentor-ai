import streamlit as st
from utils.gemini_helper import get_gemini_model
from utils.flashcard_utils import generate_flashcards, parse_flashcards


def render():
    st.title("📇 Flashcards Generator")
    st.markdown("Generate interactive flashcards from your documents to help with active recall.")

    # Provide an option to use uploaded documents or paste text
    source_option = st.radio("Select Source", ["Use Uploaded Documents", "Paste Text"])

    text_to_process = ""

    if source_option == "Use Uploaded Documents":
        if "documents" in st.session_state and len(st.session_state["documents"]) > 0:
            doc_names = [doc["name"] for doc in st.session_state["documents"]]
            selected_doc_name = st.selectbox("Select a document", doc_names)

            # Get the text for the selected document
            for doc in st.session_state["documents"]:
                if doc["name"] == selected_doc_name:
                    text_to_process = doc["text"]
                    break
        else:
            st.info("No documents uploaded yet. Go to the PDF Summarizer or Lecture Notes page to upload a file.")

    else:
        text_to_process = st.text_area("Paste text here to generate flashcards", height=200)

    if st.button("Generate Flashcards"):
        if text_to_process:
            with st.spinner("Generating flashcards using Gemini..."):
                try:
                    llm = get_gemini_model()
                    # If text is too long, trim it to avoid token limits for flashcard generation
                    # Just take the first 15000 chars as a basic safety mechanism
                    text_to_process = text_to_process[:15000]

                    flashcards_raw = generate_flashcards(text_to_process, llm)
                    flashcards = parse_flashcards(flashcards_raw)

                    if flashcards:
                        st.success(f"Successfully generated {len(flashcards)} flashcards!")
                        st.session_state["current_flashcards"] = flashcards
                    else:
                        st.error("Failed to parse flashcards. Please try again.")
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Please provide some text to generate flashcards.")

    # Display flashcards if they exist in session state
    if "current_flashcards" in st.session_state and st.session_state["current_flashcards"]:
        st.markdown("### Your Flashcards")

        for i, fc in enumerate(st.session_state["current_flashcards"]):
            with st.expander(f"Question {i+1}: {fc['question']}"):
                st.write(f"**Answer:** {fc['answer']}")
