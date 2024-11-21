from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class BaseModel:
    __abstract__ = True
    id = Column(Integer, primary_key=True)
    date_added = Column(DateTime, default=datetime.now)
    
    def __init__(self):
        self._is_deleted = False
    
    @property
    def is_deleted(self):
        return self._is_deleted
    
    @is_deleted.setter
    def is_deleted(self, value):
        self._is_deleted = value

class Products(BaseModel, db.Model):
    __tablename__ = 'products'
    
    name = Column(String(100), nullable=False)
    type = Column(String(50), nullable=False)
    category = Column(String(50), nullable=False)
    brand = Column(String(50), nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)
    description = Column(String(500))
    
    orders = relationship('Orders', back_populates='product')
    
    def __init__(self, name, type, category, brand, price, stock, description=None):
        super().__init__()
        self.name = name
        self.type = type
        self.category = category
        self.brand = brand
        self.price = price
        self.stock = stock
        self.description = description

class Customers(BaseModel, db.Model):
    __tablename__ = 'customers'
    
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(120), nullable=False, unique=True)
    # city = Column(String(50), nullable=False)
    # province Column(String(50), nullable=False)
    # postal_code = Column(String(7) nullable=False)
    
    orders = relationship('Orders', back_populates='customer')
    
    def __init__(self, first_name, last_name, email):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
       # self.city = city
       # self.province = province
       # self.postal_code = zipcode

class Orders(BaseModel, db.Model):
    __tablename__ = 'orders'
    
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    
    customer = relationship('Customers', back_populates='orders')
    product = relationship('Products', back_populates='orders')
    
    def __init__(self, customer_id, product_id, quantity):
        super().__init__()
        self.customer_id = customer_id
        self.product_id = product_id
        self.quantity = quantity