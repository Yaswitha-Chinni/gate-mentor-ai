import streamlit as st
from modules.auth import login_user

st.set_page_config(page_title="Login", page_icon="🔐")

st.title("Login to GATE Mentor AI")

# Initialize session state if not present
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if st.session_state.logged_in:
    st.success(f"You are already logged in as {st.session_state.user_name}.")
    if st.button("Logout"):
        from modules.auth import logout_user
        logout_user()
else:
    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        
        submit_button = st.form_submit_button("Login")
        
    if submit_button:
        response = login_user(email, password)
        if response["success"]:
            st.success(response["message"])
            st.rerun()
        else:
            st.error(response["message"])
