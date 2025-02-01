import gradio as gr
import requests
import socket

# API URL for the model
API_URL = "http://localhost:11434/api/generate"  # Replace with your API URL

def generate_gradio_url():
    ip_address = socket.gethostbyname(socket.gethostname())
    return f'0.0.0.0:7860'  # Gradio works better with 0.0.0.0 to allow network access

def chat_with_model(user_message, chat_history):
    if not user_message.strip() or len(user_message.strip()) < 2:
        return chat_history + [("You", user_message), ("Bot", "❌ Please enter a longer message.")]

    data = {
        "model": "deepseek-r1:1.5b",  # Replace with your actual model name
        "prompt": user_message,
        "stream": False
    }

    try:
        response = requests.post(API_URL, json=data, timeout=30)
        if response.status_code == 200:
            response_data = response.json()
            bot_reply = response_data.get("response", "⚠️ No response from the model.")
        else:
            bot_reply = f"❌ Error: {response.status_code} - {response.text}"
    except requests.exceptions.RequestException as e:
        bot_reply = f"❌ Request failed: {e}"

    return chat_history + [("You", user_message), ("Bot", bot_reply)]

def main():
    with gr.Blocks() as demo:
        chat_history = gr.State([])

        # Chatbot Component to display the messages
        chatbot = gr.Chatbot(elem_id="chatbot_area", height=600)

        # Input and Button
        message_input = gr.Textbox(placeholder="Type your message here...", label="Your Message")
        send_button = gr.Button("Send")

        # Handling send button click
        def handle_send(user_message, chat_history):
            return chat_with_model(user_message, chat_history)

        send_button.click(fn=handle_send, inputs=[message_input, chat_history], outputs=[chatbot, chat_history])

    # Launch Gradio app
    demo.launch(server_name="0.0.0.0", server_port=7860, share=False)  # Allow all devices to access

if __name__ == "__main__":
    main()
