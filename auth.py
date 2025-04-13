import streamlit as st
import database as db
from datetime import datetime

def login_form():
    """Display login form and handle login process"""
    
    # Initialize session state for login
    if "user_id" not in st.session_state:
        st.session_state.user_id = None
    if "username" not in st.session_state:
        st.session_state.username = None
    if "is_logged_in" not in st.session_state:
        st.session_state.is_logged_in = False
    
    # If user is already logged in, show logout option
    if st.session_state.is_logged_in:
        st.sidebar.write(f"👤 Logged in as: **{st.session_state.username}**")
        if st.sidebar.button("Logout"):
            logout_user()
        return True
    
    # Otherwise, show login form
    with st.sidebar.form("login_form"):
        st.header("Login / Register")
        username = st.text_input("Username")
        
        # Simple login/register that only requires username
        submit = st.form_submit_button("Login / Register")
        
        if submit and username:
            login_user(username)
            return True
    
    return False


def login_user(username):
    """Login a user with the given username"""
    # Get or create user in database
    user = db.get_or_create_user(username)
    
    # Update session state
    st.session_state.user_id = user.id
    st.session_state.username = user.username
    st.session_state.is_logged_in = True
    
    # Rerun to update UI
    st.rerun()


def logout_user():
    """Logout the current user"""
    # Clear session state
    st.session_state.user_id = None
    st.session_state.username = None
    st.session_state.is_logged_in = False
    
    # Rerun to update UI
    st.rerun()


def require_login():
    """
    Require login to access a feature.
    Returns True if user is logged in, False otherwise.
    """
    if not st.session_state.get("is_logged_in", False):
        st.warning("⚠️ You need to login to use this feature.")
        return False
    return True


def logged_in_user():
    """Get the current logged in user ID"""
    return st.session_state.get("user_id", None)