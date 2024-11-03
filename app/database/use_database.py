import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from classes.database import Database


# Example usage
def main():
    db = Database("database.db")           # Création de l'instance de la base de données et connection
    db.connect()                            
    
    # Table products
    create_products_table = '''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        brand TEXT NOT NULL,
        model TEXT NOT NULL, 
        price REAL NOT NULL,
        description TEXT,
        stock INTEGER NOT NULL,
        date_added TEXT NOT NULL DEFAULT CURRENT_DATE,
        supplier_id INTEGER NOT NULL,
        FOREIGN KEY (supplier_id) REFERENCES suppliers (id)
    )
    '''
    # Table suppliers
    create_suppliers_table = '''
    CREATE TABLE IF NOT EXISTS suppliers (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        contact TEXT NOT NULL,
        email TEXT NOT NULL,
        phone TEXT NOT NULL
    )
    '''
    # Table orders
    create_orders_table = '''
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY,
        order_date TEXT NOT NULL DEFAULT CURRENT_DATE,
        customer_id INTEGER NOT NULL,
        status TEXT NOT NULL,
        total_price REAL NOT NULL,
        FOREIGN KEY (customer_id) REFERENCES clients (id)
    )
    '''
    # Table sales
    create_sales_table = '''
    CREATE TABLE IF NOT EXISTS sales (
        id INTEGER PRIMARY KEY,
        sale_date TEXT NOT NULL DEFAULT CURRENT_DATE,
        order_id INTEGER NOT NULL,
        total_price REAL NOT NULL,
        FOREIGN KEY (order_id) REFERENCES orders (id)
    )
    '''
    # Table order_product
    create_order_product_table = '''
    CREATE TABLE IF NOT EXISTS order_product (
        id INTEGER PRIMARY KEY,
        order_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        unit_price REAL NOT NULL,
        FOREIGN KEY (order_id) REFERENCES orders (id),
        FOREIGN KEY (product_id) REFERENCES products (id)
    )
    '''

    # Table clients
    create_clients_table = '''
    CREATE TABLE IF NOT EXISTS clients (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        phone TEXT,
        address TEXT,
        password TEXT NOT NULL
    )
    '''

    # Table users 
    create_users_table = '''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        role TEXT NOT NULL CHECK (role IN ('admin', 'registered', 'visitor')),
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        last_login TEXT
    )
    '''

    # Exécution de la création des tables
    db.execute_query(create_products_table)
    db.execute_query(create_suppliers_table)
    db.execute_query(create_orders_table)
    db.execute_query(create_sales_table)
    db.execute_query(create_order_product_table)
    db.execute_query(create_clients_table)
    db.execute_query(create_users_table)

    
    # Insertion des données initiales pour chaque table
    initial_supplier_query = '''INSERT INTO suppliers (name, contact, email, phone) VALUES (?, ?, ?, ?)'''
    suppliers_data = [
        ('TechSupply Inc.', 'John Doe', 'john@techsupply.com', '+1234567890'), 
        ('Gadget World', 'Jane Smith', 'jane@gadgetworld.com', '+0987654321')]
    for supplier in suppliers_data:
        db.execute_query(initial_supplier_query, supplier)

    initial_products_query = '''INSERT INTO products (name, category, brand, model, price, description, stock, supplier_id) 
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)'''
    products_data = [
        ('Smartphone X', 'Phone', 'TechBrand', 'X1', 799.99, 'Latest smartphone model', 50, 1),
        ('Laptop Pro', 'Computer', 'CompTech', 'Pro2', 1299.99, 'High-performance laptop', 30, 2)]
    for product in products_data:
        db.execute_query(initial_products_query, product)
    
    initial_clients_query = '''INSERT INTO clients (name, email, phone, address, password) VALUES (?, ?, ?, ?, ?)'''
    clients_data = [
        ('Alice Johnson', 'alice@email.com', '+1122334455', '123 Main St, City', 'hashed_password_1'),
        ('Bob Williams', 'bob@email.com', '+5544332211', '456 Oak Ave, Town', 'hashed_password_2')]
    for client in clients_data:
        db.execute_query(initial_clients_query, client)

    

    initial_users_query = '''INSERT INTO users (username, email, password, role) VALUES (?, ?, ?, ?)'''
    users_data = [
        ('admin_user', 'admin@example.com', 'hashed_admin_password', 'admin'),
        ('regular_user', 'user@example.com', 'hashed_user_password', 'registered')
    ]
    for user in users_data:
        db.execute_query(initial_users_query, user)

    
    select_query = "SELECT * FROM users"
    users = db.fetch_all(select_query)
    print("Users:", users)
    
    db.disconnect()

if __name__ == "__main__":
    main()
