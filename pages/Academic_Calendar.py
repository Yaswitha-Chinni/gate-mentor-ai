import streamlit as st
import pandas as pd
from modules.auth import require_login
from modules.calendar_manager import save_calendar_data, get_calendar_data, simulate_extraction

st.set_page_config(page_title="Academic Calendar", page_icon="📆", layout="wide")
require_login()

st.title("📆 Academic Calendar Integration")
st.markdown("Upload your college academic calendar to automatically map out your exam dates and holidays. The AI Coach will use this to prevent scheduling heavy GATE study sessions during your college exams.")

user_id = st.session_state.user_id

# Display Existing Data
calendar = get_calendar_data(user_id)

if calendar:
    with st.container(border=True):
        st.subheader("Current Academic Calendar")
        st.success("Calendar is actively syncing with your Study Plan.")
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Semester Timeline:**")
            sem = calendar.get('semester_dates', {})
            st.write(f"Start: `{sem.get('start', 'N/A')}` | End: `{sem.get('end', 'N/A')}`")
            
            st.write("**College Exams:**")
            mid = calendar.get('mid_exams', {})
            end = calendar.get('end_exams', {})
            st.write(f"Mid Exams: `{mid.get('start', 'N/A')} to {mid.get('end', 'N/A')}`")
            st.write(f"End Exams: `{end.get('start', 'N/A')} to {end.get('end', 'N/A')}`")
            
        with col2:
            st.write("**Upcoming Holidays:**")
            holidays = calendar.get('holidays', [])
            if holidays:
                df = pd.DataFrame(holidays, columns=["Date"])
                st.dataframe(df, hide_index=True, use_container_width=True)
            else:
                st.write("No holidays detected.")
                
        if st.button("Re-upload Calendar", type="secondary"):
            # A tiny hack to let them clear it or just let the form below overwrite
            pass

st.markdown("---")
st.subheader("Upload New Calendar")

with st.form("calendar_upload_form"):
    calendar_url = st.text_input("Academic Calendar URL (Optional)")
    uploaded_file = st.file_uploader("Upload Calendar PDF", type=["pdf"])
    
    submit = st.form_submit_button("Extract & Sync Calendar")
    
if submit:
    if not calendar_url and not uploaded_file:
        st.error("Please provide either a URL or upload a PDF file.")
    else:
        with st.spinner("Extracting dates using Future-Ready AI models..."):
            # Simulate extraction for MVP
            filename = uploaded_file.name if uploaded_file else calendar_url
            extracted_data = simulate_extraction(filename)
            
            resp = save_calendar_data(user_id, calendar_url if calendar_url else "Uploaded PDF", extracted_data)
            
            if resp["success"]:
                st.success("Calendar extracted and synced successfully!")
                st.rerun()
