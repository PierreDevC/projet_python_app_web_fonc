# Création/insertion de la table produits
# Création/insertion de la table users

from models import Products
from users import User

import sqlite3

# Connect to the database
conn = sqlite3.connect('inventory.db')
cursor = conn.cursor()

# Create products table
cursor.execute('''
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    category TEXT NOT NULL,
    brand TEXT NOT NULL,
    price REAL NOT NULL,
    stock INTEGER,
    description TEXT,
    date_added TEXT NOT NULL DEFAULT CURRENT_DATE
)
''')

# Create brands table
cursor.execute('''
CREATE TABLE IF NOT EXISTS brands (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
)
''')

# Create user table
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    role TEXT NOT NULL,
    creation_date TEXT DEFAULT CURRENT_TIMESTAMP,
    last_login TEXT
)
''')

# Add 10 brands to the brands table
brands = [
    (1, 'Acer'),
    (2, 'Apple'),
    (3, 'Asus'),
    (4, 'Dell'),
    (5, 'HP'),
    (6, 'Lenovo'),
    (7, 'Microsoft'),
    (8, 'Samsung'),
    (9, 'Sony'),
    (10, 'Toshiba')
]

cursor.executemany('INSERT OR IGNORE INTO brands (id, name) VALUES (?, ?)', brands)

conn.commit()
conn.close()

print("All tables have been created successfully in the 'inventory.db' database.")
print("10 brands have been added to the brands table.")


product1 = Products("MacBook Pro", "Laptop", "Productivity", "Apple", 1999.99, 50, "High-performance laptop for professionals")
product2 = Products("Dell XPS 15", "Laptop", "Workstation", "Dell", 1799.99, 30, "Powerful workstation for content creators")
product3 = Products("Lenovo Legion", "Desktop", "Gaming", "Lenovo", 1499.99, 20, "High-end gaming desktop")
product4 = Products("HP Envy", "Laptop", "Productivity", "HP", 999.99, 100, "Sleek and efficient laptop for everyday use")
product5 = Products("Asus ROG", "Laptop", "Gaming", "Asus", 1699.99, 40, "Premium gaming laptop with high refresh rate display")

product1.add_product('inventory.db')
product2.add_product('inventory.db')
product3.add_product('inventory.db')
product4.add_product('inventory.db')
product5.add_product('inventory.db')

# Create a new user instance
new_user = User(username="john_doe", email="john@example.com", password="secure_password", role="user")

# Add the user to the database
new_user.add_user('inventory.db')




# Ajout dans la base de données


with sqlite3.connect('inventory.db') as conn:
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL,
    date_added TEXT NOT NULL DEFAULT CURRENT_DATE  
    )
    ''')

    # List of 10 products
products = [
    ("MacBook Pro", "Laptop", "Productivity", "Apple", 1999.99, 50, "High-performance laptop for professionals"),
    ("Dell XPS 15", "Laptop", "Productivity", "Dell", 1499.99, 30, "Powerful and sleek laptop for work and entertainment"),
    ("Alienware Aurora R12", "Desktop", "Gaming", "Dell", 1799.99, 20, "High-end gaming desktop with customizable RGB lighting"),
    ("HP Envy 34", "Desktop", "Workstation", "HP", 1999.99, 15, "All-in-one desktop with a large curved display"),
    ("Lenovo ThinkPad X1 Carbon", "Laptop", "Productivity", "Lenovo", 1399.99, 40, "Ultra-light business laptop with long battery life"),
    ("ASUS ROG Zephyrus G14", "Laptop", "Gaming", "Asus", 1499.99, 25, "Compact and powerful gaming laptop"),
    ("iMac 24-inch", "Desktop", "Productivity", "Apple", 1299.99, 35, "Colorful all-in-one desktop with M1 chip"),
    ("Microsoft Surface Laptop 4", "Laptop", "Productivity", "Microsoft", 999.99, 45, "Sleek and versatile laptop with touchscreen"),
    ("Acer Predator Helios 300", "Laptop", "Gaming", "Acer", 1199.99, 30, "Popular mid-range gaming laptop"),
    ("HP Z4 G4", "Desktop", "Workstation", "HP", 2499.99, 10, "High-performance workstation for demanding tasks")
]

# Connect to the database and insert products
with sqlite3.connect('inventory.db') as conn:
    cursor = conn.cursor()
    cursor.executemany('''
    INSERT INTO products (name, type, category, brand, price, stock, description)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', products)
    conn.commit()

print("10 products have been added to the database.")
