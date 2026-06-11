import streamlit as st
from modules.auth import require_login
from modules.profile_manager import get_profile, calculate_profile_completeness
from modules.gate_goal_manager import get_user_goal
from database.db import get_connection
from modules.dashboard_manager import calculate_days_remaining, get_study_streak, get_kpi_metrics, calculate_preparation_health

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")
require_login()

user_id = st.session_state.user_id
user_name = st.session_state.user_name

st.title(f"👋 Welcome back, {user_name}!")
st.markdown("Here is your GATE Preparation Overview.")

profile = get_profile(user_id)
goal = get_user_goal(user_id)
prof_comp = calculate_profile_completeness(profile) if profile else 0
has_plan = False # Can check DB if study plan exists

kpis = get_kpi_metrics(user_id)
streak = get_study_streak(user_id)
days_rem = calculate_days_remaining(goal.target_gate_year if goal else None)

# --- Top Row KPIs ---
c1, c2, c3, c4 = st.columns(4)
with c1.container(border=True):
    st.metric("🔥 Study Streak", f"{streak} Days")
with c2.container(border=True):
    st.metric("⏳ Days Remaining", days_rem if days_rem > 0 else "N/A")
with c3.container(border=True):
    st.metric("✅ Subjects Completed", kpis["subjects_completed"])
with c4.container(border=True):
    st.metric("🎯 Topics Completed", kpis["topics_completed"])

st.markdown("---")

# --- Middle Row: Preparation Health & Setup ---
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("System Resources")
    with st.container(border=True):
        r1, r2, r3, r4 = st.columns(4)
        r1.metric("🎥 Videos", kpis["videos_available"])
        r2.metric("📝 Notes", kpis["notes_available"])
        r3.metric("❓ PYQs", kpis["pyqs_available"])
        r4.metric("🎯 Practice Sets", kpis["practice_sets_available"])
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.page_link("pages/Subjects_Hub.py", label="Explore All Subjects", icon="📚")

with col2:
    st.subheader("Setup Checklist")
    with st.container(border=True):
        health = calculate_preparation_health(user_id, prof_comp, goal is not None, has_plan)
        color = "green" if health['status'] == "Excellent" else "orange" if health['status'] == "Good" else "red"
        st.markdown(f"**Overall Health:** :{color}[{health['status']}]")
        st.progress(health['score'] / 100.0)
        
        st.write("---")
        if prof_comp < 100:
            st.warning("⚠️ Profile Incomplete")
            st.page_link("pages/Profile.py", label="Complete Profile")
        else:
            st.success("✅ Profile Complete")
            
        if not goal:
            st.warning("⚠️ Goal Not Set")
            st.page_link("pages/Gate_Goal.py", label="Set Goal")
        else:
            st.success("✅ Goal Set")
