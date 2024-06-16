from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from mysql.connector import Error
import threading

app = Flask(__name__)

def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host="localhost",  # Replace with your MySQL host
            user="root",  # Replace with your MySQL username
            password="root",  # Replace with your MySQL password
            database="mansukh"  # Replace with your database name
        )
        if connection.is_connected():
            print("Connected to MySQL database")
    except Error as e:
        print(f"Error: {e}")
    return connection


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        dob = request.form['dob']
        email = request.form['email']
        phone = request.form['phone']

        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO users (username, password, dob, email, phone) VALUES (%s, %s, %s, %s, %s)",
                       (username, password, dob, email, phone))
        connection.commit()
        cursor.close()
        connection.close()

        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

def start_gradio():
    launch_chatbot()  # Ensure this function exists in gradio_app1 and launches the Gradio app

if __name__ == "__main__":
    threading.Thread(target=start_gradio).start()
    import logging
    logging.basicConfig(level=logging.DEBUG)
    app.run(debug=True)
