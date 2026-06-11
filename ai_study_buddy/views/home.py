import streamlit as st
import os


def render():
    st.title("Welcome to AI Study Buddy! 🎓")

    st.write("Current directory:", os.getcwd())
    try:
        views_dir = os.listdir("views")
        st.write("Views directory contents:", views_dir)
        print("DEBUG VIEWS:", views_dir)
    except Exception as e:
        st.write("Error reading views directory:", str(e))
        print("DEBUG VIEWS ERROR:", str(e))

    st.markdown("""
    ### Your Ultimate AI-Powered Learning Assistant

    AI Study Buddy is designed to help students learn faster and smarter. Whether you have a long PDF document or an audio recording of a lecture, we've got you covered.

    ---

    ### ✨ Features

    - **📄 PDF Summarizer**: Upload your course notes or research papers and get a concise summary in seconds.
    - **🎧 Lecture Notes**: Missed writing notes? Upload your lecture audio (MP3/WAV) and we will transcribe and structure the notes for you.
    - **📇 Flashcards Generator**: Automatically generate flashcards from your documents to help with active recall.
    - **📝 Quiz Generator**: Test your knowledge with an AI-generated multiple choice quiz based on your materials.
    - **🤖 AI Tutor**: Have a question about your uploaded notes? Ask the AI Tutor. It searches through your documents to give you a context-aware answer.

    ---

    ### 🚀 Quick Start

    1. Go to the **PDF Summarizer** or **Lecture Notes** section from the sidebar.
    2. Upload your file to process it and add it to your knowledge base.
    3. Once processed, use the **Flashcards**, **Quiz Generator**, or **AI Tutor** to learn and test your knowledge!

    ---

    ### 💻 Technology Stack

    - **Frontend**: Streamlit
    - **Backend**: Python
    - **AI Models**: Google Gemini 2.5 Flash, Gemini Embeddings, OpenAI Whisper
    - **Vector Database**: ChromaDB
    - **Frameworks**: LangChain

    """)

    st.info("👈 Select a tool from the sidebar to get started!")
