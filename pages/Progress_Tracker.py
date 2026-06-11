import streamlit as st
import pandas as pd
from modules.auth import require_login
from database.queries import get_study_plan, get_progress, get_topic_by_name
from modules.progress_manager import sync_progress_status, get_subject_progress, calculate_overall_completion

st.set_page_config(page_title="Progress Tracker", page_icon="📈", layout="wide")

# Enforce authentication
require_login()

st.title("📈 Progress Tracker")
st.markdown("Track your GATE preparation progress topic-by-topic.")

user_id = st.session_state.user_id
plans = get_study_plan(user_id)

if not plans:
    st.warning("No study plan found. Generate a study plan first.")
    st.page_link("pages/Study_Plan.py", label="Go to Study Plan Generator")
    st.stop()

# Remove revision pseudo-topics for actual progress tracking
valid_plans = [p for p in plans if p.subject_name != "Final Revision & Mock Tests"]

# --- TOP SECTION: SUMMARY & VISUALIZATIONS ---
overall_comp = calculate_overall_completion(user_id)
st.progress(overall_comp / 100.0)
st.markdown(f"**Overall Completion: {overall_comp}%**")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Subject-wise Progress")
    subj_prog = get_subject_progress(user_id)
    if subj_prog:
        chart_data = pd.DataFrame({
            "Subject": list(subj_prog.keys()),
            "Completion %": list(subj_prog.values())
        }).set_index("Subject")
        st.bar_chart(chart_data)

with col2:
    st.subheader("Status Distribution")
    status_counts = {"Completed": 0, "In Progress": 0, "Pending": 0, "Needs Revision": 0, "Not Started": 0}
    for p in valid_plans:
        if p.status in status_counts:
            status_counts[p.status] += 1
        else:
            status_counts["Not Started"] += 1
            
    dist_data = pd.DataFrame({
        "Status": list(status_counts.keys()),
        "Count": list(status_counts.values())
    }).set_index("Status")
    # Streamlit doesn't have native pie chart without plotting libraries, so we use bar_chart
    st.bar_chart(dist_data)

st.markdown("---")

# --- FILTERS & SEARCH ---
st.subheader("Topic Manager")

f_col1, f_col2, f_col3 = st.columns(3)
with f_col1:
    all_subjects = ["All Subjects"] + sorted(list(set(p.subject_name for p in valid_plans)))
    selected_subject = st.selectbox("Subject Filter", all_subjects)
    
with f_col2:
    status_options = ["All", "Not Started", "In Progress", "Completed", "Needs Revision"]
    selected_status = st.selectbox("Status Filter", status_options)

with f_col3:
    search_query = st.text_input("Search by Topic Name")

# Apply filters
filtered_plans = valid_plans
if selected_subject != "All Subjects":
    filtered_plans = [p for p in filtered_plans if p.subject_name == selected_subject]
if selected_status != "All":
    filtered_plans = [p for p in filtered_plans if p.status == selected_status]
if search_query:
    filtered_plans = [p for p in filtered_plans if search_query.lower() in p.topic_name.lower()]

st.write(f"Showing {len(filtered_plans)} topics")

# --- BULK UPDATE & TABLE ---
# Since Streamlit forms refresh the whole page, we can use a data editor or form
with st.form("progress_update_form"):
    st.write("Update Status or Study Hours")
    
    # Render table headers
    h_col1, h_col2, h_col3, h_col4, h_col5 = st.columns([2, 3, 1, 2, 2])
    h_col1.write("**Subject**")
    h_col2.write("**Topic**")
    h_col3.write("**Planned (Hrs)**")
    h_col4.write("**Status**")
    h_col5.write("**Studied (Hrs)**")
    
    # We need to map existing study hours from progress table to the UI
    raw_progress = get_progress(user_id)
    prog_map = {p.topic_id: p.study_hours for p in raw_progress}
    
    update_data = []
    
    for plan in filtered_plans:
        c1, c2, c3, c4, c5 = st.columns([2, 3, 1, 2, 2])
        c1.write(plan.subject_name)
        c2.write(plan.topic_name)
        c3.write(str(plan.planned_hours))
        
        # Current status dropdown
        idx = status_options[1:].index(plan.status) if plan.status in status_options[1:] else 0
        new_status = c4.selectbox("Status", status_options[1:], index=idx, key=f"status_{plan.plan_id}", label_visibility="collapsed")
        
        # Current studied hours
        t_id = get_topic_by_name(plan.topic_name)
        current_hrs = prog_map.get(t_id, 0) if t_id else 0
        
        new_hrs = c5.number_input("Hrs", min_value=0, value=int(current_hrs), key=f"hrs_{plan.plan_id}", label_visibility="collapsed")
        
        update_data.append({
            "plan_id": plan.plan_id,
            "topic_name": plan.topic_name,
            "old_status": plan.status,
            "new_status": new_status,
            "old_hrs": current_hrs,
            "new_hrs": new_hrs
        })
        
    submit = st.form_submit_button("Save All Updates")
    
if submit:
    changes_made = 0
    for data in update_data:
        if data["old_status"] != data["new_status"] or data["old_hrs"] != data["new_hrs"]:
            success = sync_progress_status(user_id, data["plan_id"], data["topic_name"], data["new_status"], data["new_hrs"])
            if success:
                changes_made += 1
                
    if changes_made > 0:
        st.success(f"Successfully updated {changes_made} topics! Dashboard metrics synced.")
        st.rerun()
    else:
        st.info("No changes detected.")
