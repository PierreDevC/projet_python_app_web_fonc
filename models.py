from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class BaseModel:
    # la classe de base ne peut pas être instanciée directement
    __abstract__ = True 
    id = Column(Integer, primary_key=True)
    date_added = Column(DateTime, default=datetime.now)
    
    # variable pour etat de suppression
    def __init__(self):
        self._is_deleted = False
    
    # accéder à l'état de suppression
    @property
    def is_deleted(self):
        return self._is_deleted
    
    # setter l'état de suppression
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
    
    # Relation un (produits) à plusieurs (commandes)
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
    
    # Relation un (customer) à plusieurs (orders)
    orders = relationship('Orders', back_populates='customer')
    
    def __init__(self, first_name, last_name, email):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

class Orders(BaseModel, db.Model):
    __tablename__ = 'orders'
    
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    
    # Références (foreign key) aux relation un (products, customers) à plusieurs (commandes)
    customer = relationship('Customers', back_populates='orders')
    product = relationship('Products', back_populates='orders')
    
    def __init__(self, customer_id, product_id, quantity):
        super().__init__()
        self.customer_id = customer_id
        self.product_id = product_id
        self.quantity = quantity