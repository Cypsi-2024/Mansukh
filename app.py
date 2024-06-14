from flask import Flask, render_template
import threading
from gradio_app import run_gradio

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/launch-gradio')
def launch_gradio():
    threading.Thread(target=launch_chatbot()).start()
    return "Gradio app is launching..."

if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.DEBUG)
    app.run(debug=True)
