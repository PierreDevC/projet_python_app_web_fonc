import sqlite3

def create_tables():
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    
    # Create Product table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT,
            category TEXT,
            brand TEXT,
            price REAL NOT NULL,
            stock INTEGER NOT NULL,
            description TEXT,
            date_added DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create Customer table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT,
            address TEXT
        )
    ''')
    
    # Create Orders table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            date_added DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (customer_id) REFERENCES customers(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Tables created successfully (if they didn't already exist).")

# To allow execution as a script
if __name__ == "__main__":
    create_tables()
