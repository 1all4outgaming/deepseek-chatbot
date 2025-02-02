import streamlit as st
import requests

# AI model's API endpoint (Replace with your actual API)
API_URL = "http://localhost:11434/api/generate"

# Function to interact with the AI model
def chat_with_model(user_message):
    """
    Sends the user's message to the AI model and returns the response.
    """

    # Check if the message is empty or too short
    if not user_message.strip() or len(user_message.strip()) < 2:
        return "❌ Please enter a longer message."

    # API request payload
    data = {
        "model": "deepseek-r1:1.5b",  # Replace with your AI model's name
        "prompt": user_message,
        "stream": False  # Set to True if streaming response is needed
    }

    try:
        # Send request to API
        response = requests.post(API_URL, json=data)

        # If request is successful (status 200), return AI's response
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get("response", "🤖 No response from model.")
        else:
            return f"⚠️ Error: API returned status code {response.status_code}."

    except requests.exceptions.RequestException as e:
        # Handle request failure
        return f"❌ Request Failed: {str(e)}"

# Set up Streamlit page
st.set_page_config(page_title="AI Chatbot", layout="wide")

# Apply external CSS file (style.css)
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Layout columns (to center chat in the middle)
col1, col2, col3 = st.columns([1, 3, 1])

with col2:  # Middle column for chat UI
    st.title("AI Chatbot Interface")

    # User input field with "Send" button
    user_input = st.text_input("Enter your message:", key="user-input")
    send_button = st.button("Send", key="send-button")  # Send button added

    if send_button and user_input:
        # Process message and get AI response
        bot_response = chat_with_model(user_input)

        # Display user message
        st.markdown('<div class="user-message"> <strong>You:</strong> ' + user_input + '</div>', unsafe_allow_html=True)

        # Display bot response
        st.markdown('<div class="bot-message"> <strong>Bot:</strong> ' + bot_response + '</div>', unsafe_allow_html=True)

