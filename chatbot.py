import streamlit as st
from streamlit_chat import message
import random

def mental_health_chatbot():
    st.title("💬 Mental Health Assistant")
    
    # Initialize chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
        st.session_state.chat_history.append(("bot", "Hello! I'm your mental health assistant. How are you feeling today?"))
    
    # Display chat messages
    for i, (sender, msg) in enumerate(st.session_state.chat_history):
        if sender == "user":
            message(msg, is_user=True, key=f"user_{i}")
        else:
            message(msg, key=f"bot_{i}")
    
    # User input
    user_input = st.text_input("Type your message here...", key="user_input")
    
    if user_input:
        # Add user message to chat history
        st.session_state.chat_history.append(("user", user_input))
        
        # Simple chatbot responses
        responses = {
            "stress": "It's normal to feel stressed sometimes. Have you tried deep breathing exercises?",
            "anxiety": "Anxiety can be challenging. Remember to take things one step at a time.",
            "depressed": "I'm sorry you're feeling this way. Have you considered talking to a counselor?",
            "happy": "That's wonderful to hear! What's making you feel happy today?",
            "lonely": "Feeling lonely can be tough. Would you like some suggestions for connecting with others?",
            "default": "I'm here to listen. Can you tell me more about how you're feeling?"
        }
        
        # Find the most appropriate response
        bot_response = responses["default"]
        for keyword in responses:
            if keyword in user_input.lower():
                bot_response = responses[keyword]
                break
        
        # Add bot response to chat history
        st.session_state.chat_history.append(("bot", bot_response))
        
        # Rerun to update the chat display
        st.experimental_rerun()
    
    # Resources section
    st.write("---")
    st.subheader("Mental Health Resources")
    st.markdown("""
    - [National Suicide Prevention Lifeline](https://suicidepreventionlifeline.org/)
    - [Crisis Text Line](https://www.crisistextline.org/)
    - [7 Cups - Free Online Therapy](https://www.7cups.com/)
    - [Mindfulness Exercises](https://www.mindful.org/category/meditation/mindfulness-exercises/)
    """)

mental_health_chatbot()