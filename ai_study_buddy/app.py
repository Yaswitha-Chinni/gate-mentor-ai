import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="AI Study Buddy",
    page_icon="🎓",
    layout="wide"
)

# Custom CSS for modern/clean student theme
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    h1, h2, h3 {
        color: #2c3e50;
        font-family: 'Inter', sans-serif;
    }
    .stButton>button {
        background-color: #3498db;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px 24px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #2980b9;
        color: white;
        transform: translateY(-2px);
    }
    .css-1d391kg {
        background-color: #ffffff;
    }
    .stAlert {
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

st.sidebar.title("🎓 AI Study Buddy")
st.sidebar.markdown("Your personal AI-powered learning assistant.")

import views.home
import views.pdf_summarizer
import views.audio_notes
import views.flashcards
import views.quiz_generator
import views.ai_tutor

# Navigation
st.sidebar.markdown("---")
page = st.sidebar.radio("Navigation", [
    "🏠 Home", 
    "📄 PDF Summarizer", 
    "🎧 Lecture Notes", 
    "📇 Flashcards", 
    "📝 Quiz Generator", 
    "🤖 AI Tutor"
])

if page == "🏠 Home":
    views.home.render()
elif page == "📄 PDF Summarizer":
    views.pdf_summarizer.render()
elif page == "🎧 Lecture Notes":
    views.audio_notes.render()
elif page == "📇 Flashcards":
    views.flashcards.render()
elif page == "📝 Quiz Generator":
    views.quiz_generator.render()
elif page == "🤖 AI Tutor":
    views.ai_tutor.render()
