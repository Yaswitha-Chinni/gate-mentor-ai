import streamlit as st
from modules.auth import require_login
from modules.profile_manager import get_profile
from modules.gate_goal_manager import get_user_goal, save_user_goal

st.set_page_config(page_title="GATE Goal Setup", page_icon="🎯")

# Enforce authentication
require_login()

st.title("🎯 GATE Goal Setup")
st.markdown("Define your target papers, scores, and exam timeline so the AI Coach can tailor your study plan.")

user_id = st.session_state.user_id
profile = get_profile(user_id)

if not profile:
    st.error("Profile not found. Please complete your profile first.")
    st.stop()

# Display Current Profile
with st.expander("Current Profile Summary", expanded=False):
    c1, c2 = st.columns(2)
    c1.write(f"**Name:** {profile.full_name}")
    c1.write(f"**Degree:** {profile.degree if profile.degree else 'Not set'}")
    c1.write(f"**Branch:** {profile.current_branch if profile.current_branch else 'Not set'}")
    
    c2.write(f"**College:** {profile.college_name if profile.college_name else 'Not set'}")
    c2.write(f"**Current Year:** {profile.current_year if profile.current_year else 'Not set'}")
    c2.write(f"**Graduation Year:** {profile.graduation_year if profile.graduation_year else 'Not set'}")

goal = get_user_goal(user_id)

# Edit Mode Logic
if 'goal_edit_mode' not in st.session_state:
    st.session_state.goal_edit_mode = goal is None

if not st.session_state.goal_edit_mode and goal:
    with st.container(border=True):
        st.subheader("Active GATE Goal")
        
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Target GATE Year:** {goal.target_gate_year}")
            st.write(f"**Selected Paper(s):** {goal.target_papers}")
            st.write(f"**Attempt Type:** {goal.attempt_type}")
        with col2:
            st.write(f"**Target Score:** {goal.target_score if goal.target_score else 'Not set'}")
            st.write(f"**Target Rank:** {goal.target_rank if goal.target_rank else 'Not set'}")
            
        if st.button("Edit Goal", use_container_width=True):
            st.session_state.goal_edit_mode = True
            st.rerun()
else:
    with st.container(border=True):
        st.subheader("Setup Your Goal")
        with st.form("gate_goal_form"):
            c1, c2 = st.columns(2)
            year_options = [2027, 2028, 2029, 2030, 2031]
            year_idx = year_options.index(goal.target_gate_year) if (goal and goal.target_gate_year in year_options) else 0
            target_gate_year = c1.selectbox("Target GATE Year *", year_options, index=year_idx)
            
            paper_options = ["CSE", "DA", "ECE", "EE", "ME", "CE", "CH", "IN", "PI", "XE", "XL", "Mathematics", "Statistics", "Data Science"]
            default_papers = [p.strip() for p in goal.target_papers.split(",")] if goal else []
            valid_default_papers = [p for p in default_papers if p in paper_options]
            target_papers = c2.multiselect("Target Paper(s) *", paper_options, default=valid_default_papers, help="You can select multiple combination papers like CSE + DA or EE + IN.")
            
            c3, c4, c5 = st.columns(3)
            attempt_options = ["First Attempt", "Improvement Attempt", "Repeater"]
            attempt_idx = attempt_options.index(goal.attempt_type) if (goal and goal.attempt_type in attempt_options) else 0
            attempt_type = c3.selectbox("Attempt Type *", attempt_options, index=attempt_idx)
            
            target_score = c4.number_input("Target Score (Optional)", min_value=0, max_value=1000, value=goal.target_score if goal and goal.target_score else None)
            target_rank = c5.number_input("Target Rank (Optional)", min_value=1, value=goal.target_rank if goal and goal.target_rank else None)
            
            submit_button = st.form_submit_button("Save Goal")
            
        if submit_button:
            if not target_papers:
                st.error("Please select at least one Target Paper.")
            else:
                # Smart Validation
                if profile.graduation_year and target_gate_year < profile.graduation_year:
                    st.info("ℹ️ You are planning to attempt GATE before graduation. This is allowed under current GATE eligibility rules.")
                    
                goal_data = {
                    "target_gate_year": target_gate_year,
                    "target_papers": target_papers,
                    "attempt_type": attempt_type,
                    "target_score": target_score if target_score else None,
                    "target_rank": target_rank if target_rank else None
                }
                
                response = save_user_goal(user_id, goal_data)
                
                if response["success"]:
                    st.success(response["message"])
                    st.session_state.goal_edit_mode = False
                    st.rerun()
                else:
                    st.error(response["message"])
