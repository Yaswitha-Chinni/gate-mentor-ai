import streamlit as st
from utils.gemini_helper import get_gemini_model, get_gemini_embeddings
from utils.audio_loader import transcribe_audio, generate_audio_notes
from utils.vector_store import get_vector_store, add_text_to_vector_store


def render():
    st.title("🎧 Lecture Audio to Notes")
    st.markdown("Upload your lecture audio recordings to transcribe them and generate structured notes.")

    uploaded_file = st.file_uploader("Upload Audio File", type=["mp3", "wav", "m4a"])

    if st.button("Process Audio"):
        if uploaded_file is not None:
            with st.spinner("Transcribing audio using Whisper (this may take a minute)..."):
                try:
                    transcript = transcribe_audio(uploaded_file)

                    with st.expander("View Raw Transcript"):
                        st.write(transcript)

                except Exception as e:
                    st.error(f"Failed to transcribe audio: {e}")
                    st.stop()

            if transcript:
                # Save to session state for flashcards/quiz
                if "documents" not in st.session_state:
                    st.session_state["documents"] = []
                st.session_state["documents"].append({"name": uploaded_file.name, "text": transcript})

                with st.spinner("Generating structured notes using Gemini..."):
                    try:
                        llm = get_gemini_model()
                        notes = generate_audio_notes(transcript, llm)

                        st.success("Notes Generated Successfully!")
                        st.markdown("### Structured Notes")
                        st.write(notes)

                        # Download button
                        st.download_button(
                            label="⬇️ Download Notes",
                            data=notes,
                            file_name=f"{uploaded_file.name}_notes.txt",
                            mime="text/plain"
                        )
                    except Exception as e:
                        st.error(f"Failed to generate notes: {e}")

                with st.spinner("Adding notes to Vector Database for AI Tutor..."):
                    try:
                        embeddings = get_gemini_embeddings()
                        vector_store = get_vector_store(embeddings)
                        add_text_to_vector_store(transcript, vector_store)
                        st.success("Lecture notes added to AI Tutor Knowledge Base!")
                    except Exception as e:
                        st.error(f"Failed to add notes to Vector Database: {e}")
        else:
            st.warning("Please upload an audio file first.")
