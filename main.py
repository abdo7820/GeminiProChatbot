import streamlit as st
import google.generativeai as gen_ai

# Set page config
st.set_page_config(
    page_title="Chat with Gemini!",
    page_icon="🤖",
    layout="centered",
)

# Use Streamlit secrets instead of dotenv
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]

# Configure Gemini-Pro AI
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel("gemini-1.5-flash") 

# Function to translate role names
def translate_role_for_streamlit(user_role):
    return "assistant" if user_role == "model" else user_role

# Initialize chat session
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Title
st.title("🤖 Gemini Pro - ChatBot")

# Display chat history
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        st.markdown(message.parts[0].text)

# Input field for user
user_prompt = st.chat_input("Ask Gemini...")
if user_prompt:
    # Show user message
    st.chat_message("user").markdown(user_prompt)

    # Get response from Gemini
    gemini_response = st.session_state.chat_session.send_message(user_prompt)

    # Show Gemini's response
    with st.chat_message("assistant"):
        st.markdown(gemini_response.text)
