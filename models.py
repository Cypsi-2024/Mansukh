from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from utils import mysql
import json



def get_user_model():
    class User(UserMixin):
        pass
    return User

class User(UserMixin):
    def __init__(self, id, username, password_hash, dob, email, phone):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.dob = dob
        self.email = email
        self.phone = phone

    def get(username):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()
        if user:
            user_dict = {
                'id': user[0],
                'username': user[1],
                'password_hash': user[2],
                'dob': user[3],
                'email': user[4],
                'phone': user[5]
            }
            return User(user_dict['id'], user_dict['username'], user_dict['password_hash'], user_dict['dob'], user_dict['email'], user_dict['phone'])
        return None


    @staticmethod
    def create(username, password, dob, email, phone):
        cursor = mysql.connection.cursor()
        password_hash = generate_password_hash(password)
        cursor.execute("INSERT INTO users (username, password_hash, dob, email, phone) VALUES (%s, %s, %s, %s, %s)",
                       (username, password_hash, dob, email, phone))
        mysql.connection.commit()
        cursor.close()

    def check_password(self, password):
        # Convert password_hash to string if it's not already
        if not isinstance(self.password_hash, str):
            self.password_hash = str(self.password_hash)
        
        return check_password_hash(self.password_hash, password)
    
