import streamlit as st
from utils.gemini_helper import get_gemini_model, get_gemini_embeddings
from utils.pdf_loader import extract_text_from_pdf, generate_pdf_summary
from utils.vector_store import get_vector_store, add_text_to_vector_store


def render():
    st.title("📄 PDF Summarizer")
    st.markdown("Upload a PDF document to generate a concise summary and add it to your knowledge base.")

    uploaded_file = st.file_uploader("Upload PDF File", type=["pdf"])

    if st.button("Generate Summary"):
        if uploaded_file is not None:
            with st.spinner("Extracting text from PDF..."):
                try:
                    text = extract_text_from_pdf(uploaded_file)
                except Exception as e:
                    st.error(f"Failed to read PDF: {e}")
                    st.stop()

            if text:
                # Save to session state for flashcards/quiz
                if "documents" not in st.session_state:
                    st.session_state["documents"] = []
                st.session_state["documents"].append({"name": uploaded_file.name, "text": text})

                with st.spinner("Generating summary using Gemini..."):
                    try:
                        llm = get_gemini_model()
                        summary = generate_pdf_summary(text, llm)

                        st.success("Summary Generated Successfully!")
                        st.markdown("### Summary")
                        st.write(summary)

                        # Download button
                        st.download_button(
                            label="⬇️ Download Summary",
                            data=summary,
                            file_name=f"{uploaded_file.name}_summary.txt",
                            mime="text/plain"
                        )
                    except Exception as e:
                        st.error(f"Failed to generate summary: {e}")

                with st.spinner("Adding document to Vector Database for AI Tutor..."):
                    try:
                        embeddings = get_gemini_embeddings()
                        vector_store = get_vector_store(embeddings)
                        add_text_to_vector_store(text, vector_store)
                        st.success("Document added to AI Tutor Knowledge Base!")
                    except Exception as e:
                        st.error(f"Failed to add document to Vector Database: {e}")
        else:
            st.warning("Please upload a PDF file first.")
