import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from classes.database import Database


# Example usage
def main():
    # Create an instance of Database with your database file name
    db = Database("example.db")
    
    # Connect to the database
    db.connect()
    
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
