import gradio as gr
import requests
import socket
import threading

# API URL for the model
API_URL = "http://localhost:11434/api/generate"  # Replace with your API URL

# Global variable to store the current request thread (for cancellation)
current_request_thread = None

custom_css = """
body {
    font-family: sans-serif;
    display: flex;
    flex-direction: column;
    min-height: 100vh;
    margin: 0;
    background-color: #f4f4f4;
    color: #333;
    overflow: hidden; /* Prevent scrollbars on the body */
}

#chat-container {
    flex-grow: 1;
    padding: 20px;
    overflow-y: auto;
    height: 100%; /* No fixed height, allows the chat to expand */
    word-wrap: break-word;  /* Ensure long lines of text break appropriately */
    overflow: hidden;
    display: flex;
    flex-direction: column-reverse; /* Reverse the order to keep latest messages at the bottom */
}

#input-container {
    padding: 10px 20px;
    background-color: #fff;
    border-top: 1px solid #ddd;
    display: flex; /* Use flexbox for input and buttons */
}

#input-area { /* New ID for the input area */
    flex-grow: 1; /* Input area takes up available space */
    margin-right: 10px; /* Space between input and buttons */
}

.message-wrap {
    margin-bottom: 10px;
    display: flex;
    flex-direction: column; /* Messages stack vertically */
}

.user-message, .bot-message {
    max-width: 95%; /* Messages take almost full width */
    word-wrap: break-word;
    padding: 10px 15px;
    border-radius: 15px;
    margin-bottom: 5px; /* Space between message parts */
}

.user-message {
    background-color: #e9e9e9;
    color: #333;
    align-self: flex-end;
}

.bot-message {
    background-color: #007bff;
    color: #fff;
    align-self: flex-start;
    white-space: pre-wrap; /* Preserve formatting and allow wrapping for large output */
    overflow-wrap: break-word;
    word-break: break-word; /* Allows breaking words in case of huge words */
}

#input-area .textbox {
    border: 1px solid #ccc;
    border-radius: 5px;
    padding: 10px;
    font-size: 16px;
    resize: vertical;
    min-height: 60px;
}

.gr-button {
    border-radius: 300px !important;
    padding: 8px 16px !important;
    font-size: 14px !important;
    margin: 0 5px !important;
}

.gr-button.gr-button-primary {
    background-color: #007bff !important;
    border-color: #007bff !important;
}

.gr-markdown {
    text-align: center;
    padding: 20px;
    background-color: #fff;
    border-top: 1px solid #ddd;
    margin-top: 20px;
}

.avatar-img {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    margin: 5px;
}

#cancel-btn { /* Style for the cancel button */
    background-color: #dc3545 !important; /* Red color */
    border-color: #dc3545 !important;
    color: white !important;
}

/* Hide scrollbar but keep functionality */
::-webkit-scrollbar {
    width: 0.5em;
}

::-webkit-scrollbar-track {
    background: transparent;
}

::-webkit-scrollbar-thumb {
    background-color: rgba(0, 0, 0, 0.2); /* Slightly visible thumb */
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background-color: rgba(0, 0, 0, 0.5);
}
"""

def generate_gradio_url():
    ip_address = socket.gethostbyname(socket.gethostname())
    return f'http://{ip_address}:7860'

def chat_with_model(user_message, chat_history):
    global current_request_thread

    if not user_message.strip() or len(user_message.strip()) < 2:
        return chat_history + [("You", user_message), ("Bot", "❌ Please enter a longer message.")]

    data = {
        "model": "deepseek-r1:1.5b",  # Replace with your actual model name
        "prompt": user_message,
        "stream": False  # Set to False for non-streaming, can set to True if your API supports streaming for large responses
    }

    def make_request():
        try:
            response = requests.post(API_URL, json=data, timeout=None)  # Remove timeout
            if response.status_code == 200:
                response_data = response.json()
                bot_response = response_data.get("response", "🤖 No response from model.")
            else:
                bot_response = f"⚠️ Error: API returned status code {response.status_code}."
        except requests.exceptions.RequestException as e:
            bot_response = f"❌ Request Failed: {str(e)}"
        return bot_response

    bot_response = make_request()  # Execute the request

    return chat_history + [("You", user_message), ("Bot", bot_response)]

def cancel_request():
    global current_request_thread
    if current_request_thread and current_request_thread.is_alive():
        try:
            current_request_thread.join(0.1)  # Give it a little time to stop.
            if current_request_thread.is_alive():  # Check again
                print("Request Cancellation Failed. API does not support it.")
        except Exception as e:
            print(f"Error during cancellation: {e}")
    return "Request cancelled (if possible)."


with gr.Blocks(css=custom_css) as demo:
    with gr.Column(elem_id="chat-container"):
        chatbot = gr.Chatbot(
            label="Ai-Yogesh Chat Interface",
            elem_id="chatbot",
            bubble_full_width=False,
            show_copy_button=True,
            avatar_images=(
                "https://i.postimg.cc/f3PsyYYy/icons8-ai-50.png",
                "https://cdn-icons-png.flaticon.com/512/149/149071.png"
            )
        )

    with gr.Row(elem_id="input-container"):
        with gr.Column(scale=8, elem_id="input-area"):  # Added ID for input area
            user_input = gr.Textbox(
                placeholder="Type your message...",
                show_label=False,
                container=False,
                autofocus=True,
                max_lines=5
            )
        with gr.Column(scale=2):
            send_btn = gr.Button("Send", variant="primary")
            clear_btn = gr.Button("Clear")
            cancel_btn = gr.Button("Cancel", elem_id="cancel-btn")  # Cancel button

    send_click = send_btn.click(
        fn=chat_with_model,
        inputs=[user_input, chatbot],
        outputs=chatbot
    ).then(lambda: "", outputs=user_input)

    user_input.submit(
        fn=chat_with_model,
        inputs=[user_input, chatbot],
        outputs=chatbot
    ).then(lambda: "", outputs=user_input)

    clear_btn.click(lambda: None, None, chatbot, queue=False)

    cancel_btn.click(cancel_request, None, chatbot)  # Cancel function

    gr.Markdown(f"### 🌐 Access your app at: **{generate_gradio_url()}**")

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=True,
        favicon_path="https://i.postimg.cc/f3PsyYYy/icons8-ai-50.png"
    )
