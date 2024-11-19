from datetime import datetime



class BaseModel:
    __abstract__ = True
    # à finir.... va être parent de toutes les classes




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


class Customers:
    def __init__(self, first_name, last_name, email):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
    
class Orders:
    def __init__(self, customer_id, product_id, quantity):
        self.customer_id = customer_id
        self.product_id = product_id
        self.quantity = quantity
        self.date_ordered = datetime.now().strftime("%Y-%m-%d")
        