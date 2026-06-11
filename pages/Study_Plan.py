import streamlit as st
import pandas as pd
from modules.auth import require_login
from modules.profile_manager import get_profile
from database.queries import get_goal, get_study_plan
from modules.planner import generate_study_plan, export_plan_to_csv

st.set_page_config(page_title="Study Plan Generator", page_icon="📅")

# Enforce authentication
require_login()

st.title("📅 Study Plan Generator")
st.markdown("Generate a personalized GATE preparation roadmap based on your profile and examination goals.")

user_id = st.session_state.user_id
profile = get_profile(user_id)
goal = get_goal(user_id)

if not profile:
    st.warning("Please complete your Student Profile first.")
    st.stop()
    
if not goal:
    st.warning("Please set your GATE Goal first.")
    st.stop()

# Display User Input Summary
with st.expander("Your Preparation Profile", expanded=False):
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Branch:** {profile.current_branch}")
        st.write(f"**Current Year:** {profile.current_year}")
        st.write(f"**Graduation Year:** {profile.graduation_year}")
    with col2:
        st.write(f"**Target GATE Year:** {goal.target_gate_year}")
        st.write(f"**Target Paper(s):** {goal.target_papers}")
        st.write(f"**Attempt Type:** {goal.attempt_type}")

st.markdown("---")

# Generate Plan Controls
st.subheader("Plan Generation")
intensity = st.selectbox("Study Intensity", ["Casual", "Serious", "Rank < 1000", "Rank < 100"], index=1)

if st.button("Generate / Regenerate Plan"):
    with st.spinner("Analyzing syllabus and generating roadmap..."):
        response = generate_study_plan(user_id, intensity)
        if response["success"]:
            st.success(response["message"])
            st.balloons()
        else:
            st.error(response["message"])

st.markdown("---")

# Display Current Plan
plans = get_study_plan(user_id)

if plans:
    st.subheader("Your Study Plan Summary")
    
    total_topics = len([p for p in plans if p.subject_name != "Final Revision & Mock Tests"])
    total_hours = sum(p.planned_hours for p in plans if p.planned_hours)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Topics", total_topics)
    col2.metric("Estimated Hours", total_hours)
    col3.metric("Status", "Active Plan")
    
    st.markdown("### Month-wise Roadmap")
    
    # Group by month
    months = sorted(list(set(p.month_number for p in plans)))
    for month in months:
        with st.expander(f"Month {month}", expanded=True):
            month_plans = [p for p in plans if p.month_number == month]
            # Convert to DataFrame for nice table display
            df = pd.DataFrame([{
                "Subject": p.subject_name,
                "Topic": p.topic_name,
                "Planned Hours": p.planned_hours,
                "Status": p.status
            } for p in month_plans])
            st.table(df)

    # Export Feature
    csv_data = export_plan_to_csv(plans)
    st.download_button(
        label="Download Study Plan (CSV)",
        data=csv_data,
        file_name="gate_study_plan.csv",
        mime="text/csv"
    )
else:
    st.info("No study plan generated yet. Select your intensity and click Generate Plan.")
