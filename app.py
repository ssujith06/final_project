import streamlit as st
from auth import authenticate_user, register_user, check_authenticated
import database

# Initialize database
database.init_db()

# Page config
st.set_page_config(page_title="Hostel Management System", layout="wide")

# Login/Register UI
def auth_page():
    st.title("🏠 Hostel Management System")
    
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login")
            
            if submit:
                user = authenticate_user(username, password)
                if user:
                    st.session_state.authenticated = True
                    st.session_state.user_id = user[0]
                    st.session_state.username = user[1]
                    st.experimental_rerun()
                else:
                    st.error("Invalid username or password")
    
    with tab2:
        with st.form("register_form"):
            username = st.text_input("Username")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            room_number = st.text_input("Room Number")
            phone = st.text_input("Phone Number")
            submit = st.form_submeit_button("Register")
            
            if submit:
                if password != confirm_password:
                    st.error("Passwords don't match!")
                elif register_user(username, password, email, room_number, phone):
                    st.success("Registration successful! Please login.")

# Main app flow
if not check_authenticated():
    auth_page()
else:
    # Show the main app after login
    st.sidebar.title(f"Welcome, {st.session_state.username}!")
    
    if st.sidebar.button("Logout"):
        st.session_state.authenticated = False
        st.session_state.username = None
        st.experimental_rerun()
    
    # Navigation
    page = st.sidebar.radio("Menu", ["Dashboard", "Apply Outpass", "Mental Health Chatbot"])
    
    if page == "Dashboard":
        import pages.dashboard
    elif page == "Apply Outpass":
        import pages.outpass
    elif page == "Mental Health Chatbot":
        import pages.chatbot