import streamlit as st
from modules.auth import register_user

st.set_page_config(page_title="Register", page_icon="📝")

st.title("Create Account")

# Initialize session state if not present
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if st.session_state.logged_in:
    st.info("You are already logged in. Please logout to create a new account.")
else:
    with st.form("register_form"):
        full_name = st.text_input("Full Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        
        submit_button = st.form_submit_button("Register")
        
    if submit_button:
        # Validations
        if not full_name or not email or not password or not confirm_password:
            st.error("All fields are required.")
        elif len(password) < 8:
            st.error("Password must be at least 8 characters long.")
        elif password != confirm_password:
            st.error("Passwords do not match.")
        else:
            response = register_user(full_name, email, password)
            if response["success"]:
                st.success("Registration successful! You can now proceed to Login.")
                st.balloons()
            else:
                st.error(response["message"])
