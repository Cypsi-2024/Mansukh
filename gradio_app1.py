from huggingface_hub import HfApi, HfFolder, InferenceClient
import gradio as gr

# Replace 'your_hugging_face_token' with your actual Hugging Face token
hf_token = "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"

# Save the token to the Hugging Face cache directory
HfFolder.save_token(hf_token)

# Verify the token by using it to access the Hugging Face API
api = HfApi()
user_info = api.whoami(token=hf_token)

print(f"Successfully authenticated as: {user_info['name']}")


# Inference client
# client = InferenceClient("TheBloke/Llama-2-7B-Chat-GGM")
client = InferenceClient("HuggingFaceH4/zephyr-7b-beta")


def respond(message, history, system_message):
    messages = [{"role": "system", "content": system_message}]

    for val in history:
        if val[0]:
            messages.append({"role": "user", "content": val[0]})
        if val[1]:
            messages.append({"role": "assistant", "content": val[1]})

    messages.append({"role": "user", "content": message})

    response = client.chat_completion(
        messages=messages,
        # max_tokens=max_tokens,
        stream=False,
    )

    yield response["choices"][0]["message"]["content"]

def create_chatbot_interface():
    chatbot_interface = gr.ChatInterface(
        respond,
        additional_inputs=[
            gr.Textbox(value="You are a helpful bot. Your answers are clear and concise.", label="System message"),
        #     gr.Slider(minimum=1, maximum=2048, value=512, step=1, label="Max new tokens"),
        ],
    )
    return chatbot_interface

def launch_chatbot():
    with gr.Blocks() as auth_demo:
        gr.Markdown("Welcome!")

        chatbot_interface = create_chatbot_interface()

    auth_demo.launch(debug=True, share=True)

if __name__ == "__main__":
    launch_chatbot()