import streamlit as st
from modules.auth import require_login
from modules.subject_manager import get_subject_detail_data
from database.db import get_connection

st.set_page_config(page_title="Subject Detail", page_icon="🔍", layout="wide")
require_login()

if 'selected_subject_id' not in st.session_state:
    st.warning("Please select a subject from the Subjects Hub first.")
    if st.button("Go to Subjects Hub"):
        st.switch_page("pages/Subjects_Hub.py")
    st.stop()

subject_id = st.session_state.selected_subject_id
user_id = st.session_state.user_id

detail_data = get_subject_detail_data(user_id, subject_id)

if not detail_data:
    st.error("Subject not found.")
    st.stop()

st.title(f"📖 {detail_data['subject_name']}")
if st.button("⬅️ Back to Subjects Hub", type="secondary"):
    st.switch_page("pages/Subjects_Hub.py")
    
st.markdown("---")

tab1, tab2, tab3, tab4, tab5 = st.tabs(["Topics Overview", "🎥 Videos", "📝 Notes", "❓ PYQs", "🎯 Practice Sets"])

with tab1:
    st.subheader("Topic Progress")
    # Quick visual summary
    completed = len([t for t in detail_data['topics'] if t['status'] == 'Completed'])
    total = len(detail_data['topics'])
    if total > 0:
        st.progress(completed / total)
        st.caption(f"{completed}/{total} Topics Completed")
    
    for t in detail_data['topics']:
        status_color = "gray"
        if t['status'] == "Completed": status_color = "green"
        elif t['status'] == "In Progress": status_color = "orange"
        elif t['status'] == "Needs Revision": status_color = "red"
        
        with st.container(border=True):
            st.markdown(f"**{t['topic_name']}**")
            st.markdown(f"Status: :{status_color}[{t['status']}]")

# Fetch resources for this subject
conn = get_connection()
cursor = conn.cursor()
cursor.execute("""
    SELECT r.resource_type, r.title, r.url, t.topic_name
    FROM resources r
    JOIN topics t ON r.topic_id = t.topic_id
    WHERE t.subject_id = ?
""", (subject_id,))
resources = cursor.fetchall()
conn.close()

def render_resources(res_list, r_type):
    filtered = [r for r in res_list if r[0] == r_type]
    if not filtered:
        st.info(f"No {r_type.replace('_', ' ')} resources available for this subject yet.")
        return
        
    for r in filtered:
        with st.container(border=True):
            c1, c2 = st.columns([3, 1])
            c1.markdown(f"**{r[1]}**")
            c1.caption(f"Topic: {r[3]}")
            c2.link_button("🔗 Open", r[2], use_container_width=True)

with tab2: render_resources(resources, "video")
with tab3: render_resources(resources, "notes")
with tab4: render_resources(resources, "pyq")
with tab5: render_resources(resources, "practice_question")
