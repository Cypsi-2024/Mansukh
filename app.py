from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from models import User
from gradio_app1 import launch_chatbot
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField
from wtforms.validators import DataRequired,Email, ValidationError, Regexp
import secrets
from flask_mysqldb import MySQL
import threading
import bcrypt
import json
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)


# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'mansukh'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# Initialize MySQL
mysql = MySQL(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.route('/')
def index():
    return render_template('index.html')


class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[
        DataRequired(),
        Regexp(r'^[a-zA-Z\s]+$', message="Username must contain only alphabetic characters and spaces.")
    ])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[
        DataRequired(),
        Regexp(
            r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$",
            message="Password must contain at least one uppercase letter, one lowercase letter, one number, one special character, and be at least 8 characters long."
        )
    ])
    dob = DateField("Date of Birth", format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField("Register")

    def validate_username(self, field):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username=%s", (field.data,))
        user = cursor.fetchone()
        cursor.close()
        if user:
            raise ValidationError('Username already taken')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # Get user data from the form
        username = form.username.data
        password = form.password.data
        dob = form.dob.data
        email = form.email.data
        phone = request.form['phone']

        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


        # Insert user into the database
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO users (username, password_hash, dob, email, phone) VALUES (%s, %s, %s, %s, %s)",
                       (username, hashed_password.decode('utf-8'), dob, email, phone))
        mysql.connection.commit()
        cursor.close()

        flash('Registration successful. You can now log in.', 'success')
        return redirect(url_for('login'))
    for field, errors in form.errors.items():
        for error in errors:
            flash(error, 'danger')
    return render_template('register.html', form=form)

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # Query your database to get the user's hashed password
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
        user = cursor.fetchone()
        cursor.close()
        
        # Check if the user exists and the password is correct
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
            session['user_id'] = user['id']
            flash('Logged in successfully.', 'success')
            return redirect(url_for('index'))
        else:
            flash("Invalid username or password. Please try again.", 'danger')
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash("You have been logged out successfully.")
    return redirect(url_for('login'))



@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

def start_gradio():
    launch_chatbot()  # Ensure this function exists in gradio_app1 and launches the Gradio app

if __name__ == "__main__":
    # threading.Thread(target=start_gradio).start()
    # import logging
    # logging.basicConfig(level=logging.DEBUG)
    app.run(debug=True)




