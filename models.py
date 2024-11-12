import sqlite3
from datetime import datetime
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


class BaseModel:
    __abstract__ = True
    # à finir.... va être parent de toutes les classes


class Customers:
    def __init__(self, first_name, last_name, email):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email



class Products:
    def __init__(self, name, type, category, brand, price, stock, description=None):
        self.name = name
        self.type = type
        self.category = category
        self.brand = brand
        self.price = price
        self.stock = stock
        self.description = description
        self.date_added = datetime.now().strftime("%Y-%m-%d")


    @db_connection
    def add_product(self, cursor):
        cursor.execute('''
            INSERT INTO products (name, type, category, brand, price, stock, description, date_added)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (self.name, self.type, self.category, self.brand, self.price, self.stock, self.description, self.date_added))
        self.id = cursor.lastrowid

    @db_connection
    def update_product(self, cursor):
        cursor.execute('''
            UPDATE products
            SET name = ?, type = ?, category = ?, brand = ?, price = ?, stock = ?, description = ?
            WHERE id = ?
        ''', (self.name, self.type, self.category, self.brand, self.price, self.stock, self.description, self.id))

    @staticmethod
    @db_connection
    def delete_product(cursor, product_id):
        cursor.execute('DELETE FROM products WHERE id = ?', (product_id,))

    @staticmethod
    @db_connection
    def get_product_by_id(cursor, product_id):
        cursor.execute('SELECT * FROM products WHERE id = ?', (product_id,))
        return cursor.fetchone()

    @staticmethod
    @db_connection
    def get_all_products(cursor):
        cursor.execute('SELECT * FROM products')
        return cursor.fetchall()
    
