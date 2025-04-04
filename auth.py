import sqlite3
import streamlit as st
from database import verify_password, hash_password

def authenticate_user(username, password):
    conn = sqlite3.connect('hostel.db')
    c = conn.cursor()
    
    c.execute("SELECT id, username, password FROM users WHERE username=?", (username,))
    user = c.fetchone()
    conn.close()
    
    if user and verify_password(password, user[2]):
        return user[0], user[1]  # Return user_id and username
    return None

def register_user(username, password, email, room_number, phone):
    try:
        conn = sqlite3.connect('hostel.db')
        c = conn.cursor()
        
        hashed_pw = hash_password(password)
        c.execute("INSERT INTO users (username, password, email, room_number, phone, registered_on) VALUES (?, ?, ?, ?, ?, ?)",
                 (username, hashed_pw, email, room_number, phone, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        
        conn.commit()
        return True
    except sqlite3.IntegrityError as e:
        st.error(f"Registration failed: {str(e)}")
        return False
    finally:
        conn.close()

def check_authenticated():
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'username' not in st.session_state:
        st.session_state.username = None
    return st.session_state.authenticated