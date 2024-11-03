import sqlite3
import bcrypt
from database import Database

class User:
    # constructeur utilisateur
    def __init__(self, id, username, email, password, role):
        self.id = id
        self.username = username
        self.email = email
        self.password = self._hash_password(password)
        self.role = role
    
    def _hash_password(self, password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    def check_password(self, password):
        return bcrypt.checkpw(password,encode('utf-8'), self.password)
    
    def get_role(self):
        return self.role
    
    def is_admin(self):
        return self.role == 'admin'
    
    def is_registered(self):
        return self.role == "registered"
    
    def is_visitor(self):
        return self.role == "visitor"
    
    def update_profile(self, username=None, email=None):
        if username:
            self.username = username
        if email:
            self.email = email
    
    def save_to_db(self):
        db = Database("database.db")
        db.connect()
        db.execute_query('''
        INSERT OR REPLACE INTO users (id, username, email, password, role)
        VALUES (?, ?, ?, ?, ?)
        ''', (self.id, self.username, self.email, self.password, self.role))
        db.disconnect()

    @staticmethod
    def get_user_by_id(user_id):
        db = Database("database.db")
        db.connect()
        db.execute_query('SELECT * FROM users WHERE id = ?', (user_id,))
        user_data = db.fetch_one()
        db.disconnect()
        if user_data:
            return User(*user_data)
        return None
    
    def __str__(self):
        return f"User(id={self.id}, username={self.username}, email={self.email}, role={self.role})"



    