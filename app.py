import streamlit as st
from database.db import initialize_database
from utils.theme import apply_theme

# Initialize database
try:
    initialize_database()
except Exception as e:
    print(f"Database init warning: {e}")

st.set_page_config(
    page_title="GATE Mentor AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom theme
apply_theme()

# Authentication Check
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    # Public Pages
    pg = st.navigation({
        "Authentication": [
            st.Page("pages/Login.py", title="Login", icon="🔑", default=True),
            st.Page("pages/Register.py", title="Register", icon="📝"),
        ]
    })
else:
    # Authenticated Pages
    pg = st.navigation({
        "Overview": [
            st.Page("pages/Dashboard.py", title="Dashboard", icon="📊", default=True),
            st.Page("pages/Progress_Tracker.py", title="Progress Tracker", icon="📈"),
        ],
        "Learning": [
            st.Page("pages/Subjects_Hub.py", title="Subjects Hub", icon="📚"),
            st.Page("pages/Subject_Detail.py", title="Subject Detail", icon="🔍"),
            st.Page("pages/Resources.py", title="Resource System", icon="📂"),
            st.Page("pages/Study_Plan.py", title="Study Plan", icon="📅"),
        ],
        "AI Tools": [
            st.Page("pages/AI_Study_Coach.py", title="AI Study Coach", icon="🤖"),
        ],
        "Settings & Setup": [
            st.Page("pages/Profile.py", title="Profile Setup", icon="👤"),
            st.Page("pages/Gate_Goal.py", title="Goal Setup", icon="🎯"),
            st.Page("pages/Academic_Calendar.py", title="Academic Calendar", icon="📆"),
        ]
    })

pg.run()
