import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from classes.database import Database

db = Database("database.db")  
db.connect()

select_query = "SELECT * FROM products"
users = db.fetch_all(select_query)
print("Users:", users)

db.disconnect()

