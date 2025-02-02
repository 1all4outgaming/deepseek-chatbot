import streamlit as st
import requests

# Your AI model's API URL
API_URL = "http://localhost:11434/api/generate"  # Replace with your AI model API URL

# Function to interact with the AI model
def chat_with_model(user_message):
    if not user_message.strip() or len(user_message.strip()) < 2:
        return "❌ Please enter a longer message."
    
    data = {
        "model": "deepseek-r1:1.5b",  # Replace with your model's name
        "prompt": user_message,
        "stream": False  # Set to True if your API supports streaming responses
    }
    
    try:
        response = requests.post(API_URL, json=data)
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get("response", "🤖 No response from model.")
        else:
            return f"⚠️ Error: API returned status code {response.status_code}."
    except requests.exceptions.RequestException as e:
        return f"❌ Request Failed: {str(e)}"

# Set the page layout to wide to maximize the space
st.set_page_config(page_title="AI Chatbot", layout="wide")

# Use columns to control layout
col1, col2, col3 = st.columns([1, 3, 1])  # Use a 3-column layout, center the middle column

with col2:  # Middle column for chat interface
    st.title("AI Chatbot Interface", anchor=None)

    # Create a text input box at the bottom of the page
    user_input = st.text_input("You: ", "")

    if user_input:
        # When the user enters a message, interact with the model
        bot_response = chat_with_model(user_input)

        # Display user message and bot response, centered in the middle column
        st.markdown(f"<div style='text-align: center; font-size: 12px; padding-top: 20%;'>**You**: {user_input}</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='text-align: center; font-size: 12px; padding-top: 10px;'>**Bot**: {bot_response}</div>", unsafe_allow_html=True)
