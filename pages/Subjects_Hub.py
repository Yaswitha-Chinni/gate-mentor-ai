import streamlit as st
from modules.auth import require_login
from modules.subject_manager import get_subjects_hub_data
from modules.gate_goal_manager import get_user_goal

st.set_page_config(page_title="Subjects Hub", page_icon="📚", layout="wide")
require_login()

st.title("📚 Subjects Hub")
st.markdown("Your entire GATE syllabus organized by subject. Click any subject to dive into topics and resources.")

user_id = st.session_state.user_id
goal = get_user_goal(user_id)

if not goal:
    st.warning("Please setup your GATE Goals first.")
    st.stop()

target_papers = [p.strip() for p in goal.target_papers.split(",")]

subjects_data = get_subjects_hub_data(user_id)

# Filter subjects by selected papers
# Note: For MVP we mapped existing subjects to CSE.
filtered_subjects = [s for s in subjects_data if s["paper_name"] in target_papers]

# If user chose a paper like DA and we have no DA subjects yet, show a fallback message
if not filtered_subjects:
    st.info(f"Currently, the knowledge base is optimizing subjects for {goal.target_papers}. We are displaying generic subjects for you to explore the UI.")
    filtered_subjects = subjects_data

cols = st.columns(3)
for idx, subj in enumerate(filtered_subjects):
    col = cols[idx % 3]
    with col.container(border=True):
        st.subheader(subj["subject_name"])
        st.progress(subj["progress"] / 100.0)
        st.caption(f"**Progress:** {subj['progress']}%")
        
        st.write(f"**Total Topics:** {subj['total_topics']}")
        st.write(f"**Completion Deadline:** {subj['deadline']}")
        
        rc = subj["resources"]
        st.write(f"🎥 {rc['video']} Videos | 📝 {rc['notes']} Notes")
        st.write(f"❓ {rc['pyq']} PYQs | 🎯 {rc['practice_question']} Practice")
        
        if st.button("View Details", key=f"subj_btn_{subj['subject_id']}", use_container_width=True):
            st.session_state.selected_subject_id = subj['subject_id']
            st.switch_page("pages/Subject_Detail.py")
