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

    








    # Example of creating a table
    create_table_query = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL
    );
    """
    db.execute_query(create_table_query)
    
    # Example of inserting data
    insert_query = "INSERT INTO users (name, email) VALUES (?, ?)"
    db.execute_query(insert_query, ("Alice", "alice@example.com"))
    
    # Fetch data
    select_query = "SELECT * FROM users"
    users = db.fetch_all(select_query)
    print("Users:", users)
    
    # Disconnect from the database
    db.disconnect()

# Run the main function
if __name__ == "__main__":
    main()
