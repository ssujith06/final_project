import streamlit as st
from datetime import datetime
from database import create_connection

def apply_outpass():
    st.title("📝 Apply for Outpass")
    
    with st.form("outpass_form"):
        reason = st.selectbox("Reason", 
                             ["Going Home", "Medical", "Personal Work", "Other"])
        departure_date = st.date_input("Departure Date", min_value=datetime.today())
        return_date = st.date_input("Return Date", min_value=datetime.today())
        details = st.text_area("Additional Details")
        
        submitted = st.form_submit_button("Submit Application")
        
        if submitted:
            if return_date <= departure_date:
                st.error("Return date must be after departure date")
            else:
                conn = create_connection()
                if conn is not None:
                    try:
                        cursor = conn.cursor()
                        cursor.execute("INSERT INTO outpasses (student_id, reason, departure_date, return_date) VALUES (?, ?, ?, ?)",
                                     (st.session_state.user_id, reason, departure_date.strftime('%Y-%m-%d'), 
                                      return_date.strftime('%Y-%m-%d')))
                        conn.commit()
                        st.success("Outpass application submitted successfully!")
                    except Exception as e:
                        st.error(f"Error: {e}")
                    finally:
                        conn.close()

apply_outpass()