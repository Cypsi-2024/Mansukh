import gradio as gr
from huggingface_hub import InferenceClient

# Placeholder for a user database
user_db = {}

# Inference client
client = InferenceClient("HuggingFaceH4/zephyr-7b-beta")

def signup(username, password):
    if username in user_db:
        return "Username already exists. Please choose another one."
    user_db[username] = password
    return "Signup successful. You can now log in."

def login(username, password):
    if username not in user_db:
        return False, "Username does not exist. Please sign up."
    if user_db[username]!= password:
        return False, "Incorrect password. Please try again."
    return True, "Login successful. You can now access the chatbot."

def respond(message, history, system_message, max_tokens, temperature, top_p):
    messages = [{"role": "system", "content": system_message}]

    for val in history:
        if val[0]:
            messages.append({"role": "user", "content": val[0]})
        if val[1]:
            messages.append({"role": "assistant", "content": val[1]})

    messages.append({"role": "user", "content": message})

    response = ""

    for message in client.chat_completion(
        messages,
        max_tokens=max_tokens,
        stream=True,
        temperature=temperature,
        top_p=top_p,
    ):
        token = message.choices[0].delta.content

        response += token
        yield response

def create_chatbot_interface():
    chatbot_interface = gr.ChatInterface(
        respond,
        additional_inputs=[
            gr.Textbox(value="You are a friendly Chatbot.", label="System message"),
            gr.Slider(minimum=1, maximum=2048, value=512, step=1, label="Max new tokens"),
            # gr.Slider(minimum=0.1, maximum=4.0, value=0.7, step=0.1, label="Temperature"),
            # gr.Slider(minimum=0.1, maximum=1.0, value=0.95, step=0.05, label="Top-p (nucleus sampling)"),
        ],
    )
    return chatbot_interface

# Define the function to be called on button click
def create_and_launch_chatbot():
    chatbot_interface = create_chatbot_interface()

def show_signup_or_login():
    authenticated = gr.State(False)

    def handle_login(username, password):
        authenticated.value, message = login(username, password)
        # Update the visibility of the launch button
        launch_button_update = gr.update(visible=authenticated.value)
        return message, launch_button_update

    with gr.Blocks() as auth_demo:
        gr.Markdown("Welcome!")
        with gr.Tabs():
            with gr.TabItem("Sign Up"):
                signup_username = gr.Textbox(label="Username")
                signup_password = gr.Textbox(type="password", label="Password")
                signup_button = gr.Button("Sign Up")
                signup_output = gr.Textbox(label="Signup Status")

                signup_button.click(fn=signup, inputs=[signup_username, signup_password], outputs=signup_output)

            with gr.TabItem("Log In"):
                login_username = gr.Textbox(label="Username")
                login_password = gr.Textbox(type="password", label="Password")
                login_button = gr.Button("Log In")
                login_output = gr.Textbox(label="Login Status")

                launch_button = gr.Button("Launch Chatbot", visible=False)

                login_button.click(fn=handle_login, inputs=[login_username, login_password], outputs=[login_output, launch_button])

        chatbot_interface = create_chatbot_interface()

        launch_button.click(fn=create_and_launch_chatbot, inputs=None, outputs=None)

    auth_demo.launch(debug=True)

if __name__ == "__main__":
    show_signup_or_login()
