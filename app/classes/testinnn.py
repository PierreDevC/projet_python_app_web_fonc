from database import Database
from user import User

db = Database("database.db")  
try:
    db.connect()

    # Select all products
    products_query = "SELECT * FROM products"
    products = db.fetch_all(products_query)
    print("Products:", products)

    # Create a new user
    new_user = User(1, "john_doe", "john@example.com", "password123", "registered")
    new_user.save_to_db()
    print(new_user)

    # Retrieve the user by ID
    retrieved_user = User.get_user_by_id(1)
    if retrieved_user:
        print(retrieved_user)
        # Check password
        print("Password check:", retrieved_user.check_password("password123"))
    else:
        raise ValueError("User not found")
finally:
    db.disconnect()
