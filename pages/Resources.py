import streamlit as st
import pandas as pd
from modules.auth import require_login
from modules.resource_manager import get_all_resources, toggle_bookmark, get_user_bookmarks, rate_resource, get_resource_ratings

st.set_page_config(page_title="Resources System", page_icon="📂", layout="wide")
require_login()

st.title("📂 Study Resources System")
st.markdown("Find the best videos, notes, PYQs, and practice questions. Organized perfectly for your GATE preparation.")

all_resources = get_all_resources()

if not all_resources:
    st.info("No resources available right now. Please check back later.")
    st.stop()

# Build Hierarchy Filters
df = pd.DataFrame(all_resources)

# Hierarchy: Paper -> Subject -> Topic -> Resource Type
with st.container(border=True):
    st.subheader("Filter Resources")
    c1, c2, c3, c4 = st.columns(4)
    
    papers = df['paper_name'].unique().tolist()
    selected_paper = c1.selectbox("1. Select Paper", ["All Papers"] + papers)
    
    if selected_paper != "All Papers":
        df = df[df['paper_name'] == selected_paper]
        
    subjects = df['subject_name'].unique().tolist()
    selected_subject = c2.selectbox("2. Select Subject", ["All Subjects"] + subjects)
    
    if selected_subject != "All Subjects":
        df = df[df['subject_name'] == selected_subject]
        
    topics = df['topic_name'].unique().tolist()
    selected_topic = c3.selectbox("3. Select Topic", ["All Topics"] + topics)
    
    if selected_topic != "All Topics":
        df = df[df['topic_name'] == selected_topic]
        
    types = df['resource_type'].unique().tolist()
    type_display = {t: t.replace('_', ' ').title() for t in types}
    selected_type = c4.selectbox("4. Resource Type", ["All Types"] + [type_display[t] for t in types])
    
    if selected_type != "All Types":
        # reverse lookup
        for k, v in type_display.items():
            if v == selected_type:
                df = df[df['resource_type'] == k]
                break

user_bookmarks = get_user_bookmarks(st.session_state.user_id)
ratings_dict = get_resource_ratings()

st.markdown("---")

if df.empty:
    st.warning("No resources match your filters.")
else:
    cols = st.columns(3)
    for idx, row in df.iterrows():
        col = cols[idx % 3]
        with col.container(border=True):
            st.markdown(f"**{row['title']}**")
            st.caption(f"{row['paper_name']} > {row['subject_name']} > {row['topic_name']}")
            
            icon = "📄"
            if row['resource_type'] == "video": icon = "🎥"
            elif row['resource_type'] == "pyq": icon = "❓"
            elif row['resource_type'] == "practice_question": icon = "🎯"
            
            st.write(f"{icon} {row['resource_type'].replace('_', ' ').title()}")
            
            avg_rating = ratings_dict.get(row['resource_id'], 0.0)
            st.write(f"⭐ {avg_rating}/5.0")
            
            st.link_button("Open Resource", row['url'], use_container_width=True)
            
            # Bookmark logic
            is_bookmarked = row['resource_id'] in user_bookmarks
            btn_label = "Unbookmark ❌" if is_bookmarked else "Bookmark 🔖"
            if st.button(btn_label, key=f"bm_{row['resource_id']}", use_container_width=True):
                toggle_bookmark(st.session_state.user_id, row['resource_id'])
                st.rerun()
                
            # Rating logic
            with st.popover("Rate"):
                rating = st.slider("Your Rating", 1, 5, 5, key=f"slider_{row['resource_id']}")
                if st.button("Submit", key=f"rate_{row['resource_id']}"):
                    rate_resource(st.session_state.user_id, row['resource_id'], rating)
                    st.success("Rated!")
                    st.rerun()
