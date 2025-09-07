import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai

# Load environment variables
load_dotenv()

# Configure Streamlit page
st.set_page_config(
    page_title="Chat with Gemini!",
    page_icon="🤖",
    layout="centered",
)

# Get API key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    st.error("⚠️ Missing API key! Please set GOOGLE_API_KEY in your .env file.")
    st.stop()

# Configure Gemini model
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel("gemini-1.5-flash")  # أو gemini-1.5-pro

# Translate roles for Streamlit chat
def translate_role_for_streamlit(user_role):
    return "assistant" if user_role == "model" else user_role

# Initialize chat session
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Title
st.title("🤖 Gemini Pro - ChatBot")

# Display history
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        st.markdown(message.parts[0].text)

# User input
user_prompt = st.chat_input("Ask Gemini...")
if user_prompt:
    # Display user message
    st.chat_message("user").markdown(user_prompt)

    # Send to Gemini
    gemini_response = st.session_state.chat_session.send_message(user_prompt)

    # Display Gemini response
    with st.chat_message("assistant"):
        st.markdown(gemini_response.text)
