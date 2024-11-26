# Fichier : database_script.py
# Projet : Application Web Fonctionelle
# Auteurs : Pierre-Sylvestre Cypré, Aboubacar Sidiki Doumbouya
# Date : 5 Novembre 2024
# Objectif et description : Sert à tester la base de données Inventory en créant les tables et en ajoutant les données



import sqlite3

def create_and_populate_tables():
    with sqlite3.connect("inventory.db") as conn:
        cursor = conn.cursor()

        # Create tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                type TEXT NOT NULL,
                category TEXT NOT NULL,
                brand TEXT NOT NULL,
                price REAL NOT NULL,
                stock INTEGER NOT NULL,
                description TEXT,
                date_added TEXT NOT NULL DEFAULT CURRENT_DATE
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                date_added TEXT NOT NULL DEFAULT CURRENT_DATE
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                date_added TEXT NOT NULL DEFAULT CURRENT_DATE,
                FOREIGN KEY (customer_id) REFERENCES customers (id),
                FOREIGN KEY (product_id) REFERENCES products (id)
            )
        ''')

        # Insert sample data into products
        cursor.executemany('''
            INSERT INTO products (name, type, category, brand, price, stock, description)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', [
            ("Predator Orion", "desktop", "gaming", "Acer", 1500.00, 10, "High-performance gaming desktop"),
            ("MacBook Pro", "laptop", "productivity", "Apple", 2400.00, 15, "Powerful productivity laptop"),
            ("ROG Strix", "desktop", "gaming", "Asus", 1800.00, 12, "Gaming desktop with RGB lighting"),
            ("Inspiron 15", "laptop", "productivity", "Dell", 850.00, 20, "Affordable productivity laptop"),
            ("Legion Tower", "desktop", "gaming", "Lenovo", 1600.00, 8, "Gaming desktop with powerful GPU"),
        ])

        # Insert sample data into customers
        cursor.executemany('''
            INSERT INTO customers (first_name, last_name, email)
            VALUES (?, ?, ?)
        ''', [
            ("Alice", "Smith", "alice.smith@example.com"),
            ("Bob", "Johnson", "bob.johnson@example.com"),
            ("Charlie", "Brown", "charlie.brown@example.com"),
            ("Dana", "White", "dana.white@example.com"),
            ("Eve", "Davis", "eve.davis@example.com"),
        ])

        # Insert sample data into orders
        cursor.executemany('''
            INSERT INTO orders (customer_id, product_id, quantity)
            VALUES (?, ?, ?)
        ''', [
            (1, 1, 1),
            (2, 3, 2),
            (3, 5, 1),
            (4, 2, 3),
            (5, 4, 1),
        ])

        conn.commit()

if __name__ == "__main__":
    create_and_populate_tables()
    print("Tables created and populated with sample data.")
