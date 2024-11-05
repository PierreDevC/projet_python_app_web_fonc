import sqlite3
from datetime import datetime
import bcrypt
from functools import wraps

def db_connection(func):
    @wraps(func)
    def wrapper(self, db_path, *args, **kwargs):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        result = func(self, cursor, *args, **kwargs)
        conn.commit()
        conn.close()
        return result
    return wrapper

class User:
    def __init__(self, username, email, password, role="user"):
        self.username = username
        self.email = email
        self.password = self.hash_password(password)
        self.role = role
        self.creation_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.last_login = None

    # Hashage du mot-de-passe
    @staticmethod
    def hash_password(password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # Fonctions CRUD
    @db_connection
    def add_user(self, cursor):
        cursor.execute('''
            INSERT INTO users (username, email, password, role, creation_date)
            VALUES (?, ?, ?, ?, ?)
        ''', (self.username, self.email, self.password, self.role, self.creation_date))
        self.id = cursor.lastrowid

    @db_connection
    def update_user(self, cursor):
        cursor.execute('''
            UPDATE users
            SET username = ?, email = ?, password = ?, role = ?
            WHERE id = ?
        ''', (self.username, self.email, self.password, self.role, self.id))

    @db_connection
    def delete_user(cursor, user_id):
        cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))

    @staticmethod
    @db_connection
    def get_user_by_id(cursor, user_id):
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        return cursor.fetchone()
    
    @staticmethod
    @db_connection
    def get_all_users(cursor):
        cursor.execute('SELECT * FROM users')
        return cursor.fetchall()


    # Fonctions de vérification
    @staticmethod
    @db_connection
    def username_exists(cursor, username):
        cursor.execute('SELECT COUNT(*) FROM users WHERE username = ?', (username,))
        return cursor.fetchone()[0] > 0
    
    @staticmethod
    @db_connection
    def email_exists(cursor, email):

        cursor.execute('SELECT COUNT(*) FROM users WHERE email = ?', (email,))
        return cursor.fetchone()[0] > 0
    
    @db_connection
    def update_last_login(self, cursor):
        self.last_login = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute('UPDATE users SET last_login = ? WHERE id = ?', (self.last_login, self.id))

    @staticmethod
    def verify_password(hashed_password, user_password):
        return bcrypt.checkpw(user_password.encode('utf-8'), hashed_password.encode('utf-8'))