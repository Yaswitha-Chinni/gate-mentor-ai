import bcrypt
import streamlit as st
from database.queries import create_user, get_user_by_email
from database.models import User

def hash_password(password: str) -> str:
    """Hashes a password using bcrypt."""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(password: str, hashed_password: str) -> bool:
    """Verifies a password against its bcrypt hash."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def register_user(full_name: str, email: str, password: str) -> dict:
    """Registers a new user after validation."""
    if not full_name or not email or not password:
        return {"success": False, "message": "All fields are required."}
    
    # Check if email exists
    existing_user = get_user_by_email(email)
    if existing_user:
        return {"success": False, "message": "Email already registered."}
    
    hashed_pw = hash_password(password)
    
    new_user = User(
        full_name=full_name,
        email=email,
        password_hash=hashed_pw
    )
    
    user_id = create_user(new_user)
    if user_id:
        return {"success": True, "message": "Registration successful."}
    else:
        return {"success": False, "message": "Database error occurred during registration."}

def login_user(email: str, password: str) -> dict:
    """Authenticates a user and sets session state."""
    if not email or not password:
        return {"success": False, "message": "Email and Password are required."}
        
    user = get_user_by_email(email)
    if not user:
        return {"success": False, "message": "Invalid email or password."}
        
    if verify_password(password, user.password_hash):
        st.session_state.logged_in = True
        st.session_state.user_id = user.user_id
        st.session_state.user_email = user.email
        st.session_state.user_name = user.full_name
        return {"success": True, "message": "Login successful."}
    else:
        return {"success": False, "message": "Invalid email or password."}

def logout_user():
    """Clears the session and logs out the user."""
    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.user_email = None
    st.session_state.user_name = None
    
    # Rerun to clear UI states and redirect via require_login if needed
    st.rerun()

def require_login():
    """Helper to enforce route protection. Redirects to Login if not authenticated."""
    if 'logged_in' not in st.session_state or not st.session_state.logged_in:
        st.warning("You must be logged in to access this page.")
        st.stop()
