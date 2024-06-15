from flask import Flask, render_template
import threading
from gradio_app1 import launch_chatbot

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


@app.route('/chatbot')
def chatbot():   
    return render_template('chatbot.html')



if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.DEBUG)
    app.run(debug=True)

