import streamlit as st
from modules.auth import require_login
from modules.profile_manager import get_profile, save_profile, calculate_profile_completeness

st.set_page_config(page_title="Student Profile", page_icon="🎓")

# Enforce authentication
require_login()

st.title("🎓 Student Academic Profile")
st.markdown("Complete your academic profile to receive personalized GATE preparation plans.")

# Load profile data
user_id = st.session_state.user_id
profile = get_profile(user_id)

# Profile Completeness
completeness = calculate_profile_completeness(profile)
st.progress(completeness / 100.0)
st.markdown(f"**Profile Completeness: {completeness}%**")

st.markdown("---")

# Display Mode vs Edit Mode
if 'edit_mode' not in st.session_state:
    st.session_state.edit_mode = completeness < 100

if not st.session_state.edit_mode:
    # Summary Card
    with st.container(border=True):
        st.subheader("Profile Summary")
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Name:** {profile.full_name}")
            st.write(f"**Email:** {profile.email}")
            st.write(f"**College:** {profile.college_name if profile.college_name else 'Not Set'}")
            if profile.college_website:
                st.write(f"**College Website:** {profile.college_website}")
        with col2:
            st.write(f"**Degree:** {profile.degree if profile.degree else 'Not Set'}")
            st.write(f"**Branch:** {profile.current_branch if profile.current_branch else 'Not Set'}")
            st.write(f"**Current Year/Sem:** {profile.current_year} - {profile.current_semester}")
            st.write(f"**Graduation Year:** {profile.graduation_year}")
            
    if st.button("Edit Profile", use_container_width=True):
        st.session_state.edit_mode = True
        st.rerun()

else:
    # Edit Profile Form
    with st.container(border=True):
        st.subheader("Personal Information (Read Only)")
        st.info(f"**Name:** {st.session_state.user_name}  \n**Email:** {st.session_state.user_email}")
        
        st.subheader("Academic Information")
        with st.form("profile_form"):
            c1, c2 = st.columns(2)
            college_name = c1.text_input("College Name *", value=profile.college_name if profile.college_name else "")
            college_website = c2.text_input("College Website (Optional)", value=profile.college_website if profile.college_website else "")
            
            c3, c4 = st.columns(2)
            degree_options = ["B.Tech", "BE", "BSc", "MSc", "MCA", "Dual Degree"]
            degree_idx = degree_options.index(profile.degree) if profile.degree in degree_options else 0
            degree = c3.selectbox("Degree Program *", degree_options, index=degree_idx)
            
            # Hybrid Branches (Multi-Select)
            branch_options = ["CSE", "CSM", "CSD", "AI&ML", "AI&DS", "IT", "ECE", "EEE", "Mechanical", "Civil", "Mathematics", "Data Science", "Other"]
            default_branches = profile.current_branch.split(", ") if profile.current_branch else []
            valid_branches = [b for b in default_branches if b in branch_options]
            current_branches = c4.multiselect("Current Branch(es) *", branch_options, default=valid_branches, help="Select multiple if you are in a hybrid or dual degree branch.")
            
            c5, c6, c7 = st.columns(3)
            year_options = ["First Year", "Second Year", "Third Year", "Fourth Year", "Fifth Year"]
            year_idx = year_options.index(profile.current_year) if profile.current_year in year_options else 0
            current_year = c5.selectbox("Current Academic Year *", year_options, index=year_idx)
            
            sem_options = ["Semester 1", "Semester 2", "Semester 3", "Semester 4", "Semester 5", "Semester 6", "Semester 7", "Semester 8", "Semester 9", "Semester 10"]
            sem_idx = sem_options.index(profile.current_semester) if profile.current_semester in sem_options else 0
            current_semester = c6.selectbox("Current Semester *", sem_options, index=sem_idx)
            
            grad_options = list(range(2025, 2036))
            grad_idx = grad_options.index(profile.graduation_year) if profile.graduation_year in grad_options else 0
            graduation_year = c7.selectbox("Graduation Year *", grad_options, index=grad_idx)
            
            submit_button = st.form_submit_button("Save Profile")
            
        if submit_button:
            if not current_branches:
                st.error("Please select at least one branch.")
            else:
                profile_data = {
                    "college_name": college_name,
                    "college_website": college_website,
                    "degree": degree,
                    "current_branch": ", ".join(current_branches),
                    "current_year": current_year,
                    "current_semester": current_semester,
                    "graduation_year": graduation_year
                }
                
                response = save_profile(user_id, profile_data)
                if response["success"]:
                    st.success(response["message"])
                    st.session_state.edit_mode = False
                    st.rerun()
                else:
                    st.error(response["message"])
