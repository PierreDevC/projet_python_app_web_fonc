# Fichier : models.py
# Projet : Application Web Fonctionelle
# Auteurs : Pierre-Sylvestre Cypré, Aboubacar Sidiki Doumbouya
# Date : 11 Novembre 2024
# Objectif et description : Création des classes et des tables Products, Customer et Orders 
# muni de leurs propres fonctions afin qu'elles soient éxecutées dans l'application (app.py)
# Chaque classe est muni de fonctions CRUD (Create, Read, Update, Delete)
# Toutes les classes héritent d'une classe nommée BaseModel
# cls fait référence à la classe grâce à la méthode classmethod

import sqlite3
from datetime import datetime

class BaseModel:
    def __init__(self):
        self._is_deleted = False
        self.date_added = datetime.now()
    
    # propriété perméttant de savoir si l'objet a été supprimé
    @property
    def is_deleted(self):
        return self._is_deleted
    
    # setter prenant en paramètre une valeur et assigner une nouvelle valeur pour la propriété is_deleted
    @is_deleted.setter
    def is_deleted(self, value):
        self._is_deleted = value

    # méthode statique associée à la classe perméttant de se connecter à la base de données 
    @staticmethod
    def get_db():
        conn = sqlite3.connect('inventory.db')
        conn.row_factory = sqlite3.Row
        return conn

# méthode 'super' permet d'accéder aux méthodes de la classe parente
class Products(BaseModel):
    def __init__(self, name, type, category, brand, price, stock, description=None):
        super().__init__()
        self.name = name
        self.type = type
        self.category = category
        self.brand = brand
        self.price = price
        self.stock = stock
        self.description = description

    # prendre tous les produits de la table produit
    # cls représente la classe
    @classmethod
    def get_all(cls):
        conn = cls.get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM products')
        rows = cursor.fetchall()
        conn.close()
        return rows

    # prendre le prouit par id
    @classmethod
    def get_by_id(cls, id):
        conn = cls.get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM products WHERE id = ?', (id,))
        product = cursor.fetchone()
        conn.close()
        return product

    # sauvegarder le produit (add_product)
    def save(self):
        conn = self.get_db()
        cursor = conn.cursor()
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
            INSERT INTO products (name, type, category, brand, price, stock, description)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (self.name, self.type, self.category, self.brand, self.price, self.stock, self.description))
        conn.commit()
        conn.close()

    # effacer le produit 
    @staticmethod
    def delete(id):
        conn = BaseModel.get_db()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM products WHERE id = ?', (id,))
        conn.commit()
        conn.close()

    # mettre à jour le produit
    @staticmethod
    def update(id, data):
        conn = BaseModel.get_db()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE products 
            SET name=?, type=?, category=?, brand=?, price=?, stock=?, description=?
            WHERE id=?
        ''', (data['name'], data['type'], data['category'], data['brand'], 
              data['price'], data['stock'], data['description'], id))
        conn.commit()
        conn.close()

    # filtrer le produit (type, catégorie, marque et barre de recherche)
    # créer deux listes vides
    # regarde si type, categorie, marque et search on été ajouté dans le formulaire html et ajoute le paramètre
    # si il y a des conditions, on ajoute WHERE et AND
    # On execute la requête avec cursor avec la requête sql (query) et les (paramètres) comme dans name, type (?, ?, ?, ?)...

    @classmethod
    def filter_products(cls, type=None, category=None, brand=None, search=None):
        conn = cls.get_db()
        cursor = conn.cursor()
        
        query = "SELECT * FROM products"
        conditions = []
        params = []

        if type:
            conditions.append("type = ?")
            params.append(type)
        if category:
            conditions.append("category = ?")
            params.append(category)
        if brand:
            conditions.append("brand = ?")
            params.append(brand)
        if search:
            conditions.append("name LIKE ?")
            params.append(f"%{search}%")

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        return rows

    # mise à jour du stock, prend la quantité et le modifie à l'id spécifié
    @staticmethod
    def update_stock(id, quantity):
        conn = BaseModel.get_db()
        cursor = conn.cursor()
        cursor.execute('UPDATE products SET stock = stock + ? WHERE id = ?', (quantity, id))
        conn.commit()
        conn.close()

class Customers(BaseModel):
    def __init__(self, first_name, last_name, email):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

    # retourner tous les clients. class method
    @classmethod
    def get_all(cls):
        conn = cls.get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM customers')
        rows = cursor.fetchall()
        conn.close()
        return rows

    # prend le id du client
    @classmethod
    def get_by_id(cls, id):
        conn = cls.get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM customers WHERE id = ?', (id,))
        customer = cursor.fetchone()
        conn.close()
        return customer

    # sauvegarde le client (add_customer)
    def save(self):
        conn = self.get_db()
        cursor = conn.cursor()
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
            INSERT INTO customers (first_name, last_name, email)
            VALUES (?, ?, ?)
        ''', (self.first_name, self.last_name, self.email))
        conn.commit()
        conn.close()

    # méthode statique à la classe pour effacer le client selon l'id fourni
    @staticmethod
    def delete(id):
        conn = BaseModel.get_db()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM customers WHERE id = ?', (id,))
        conn.commit()
        conn.close()

    # méthode statique qui met à jour le client selon l'id fourni
    @staticmethod
    def update(id, data):
        conn = BaseModel.get_db()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE customers 
            SET first_name=?, last_name=?, email=?
            WHERE id=?
        ''', (data['first_name'], data['last_name'], data['email'], id))
        conn.commit()
        conn.close()

    # méthode de classe qui va filtrer le client selon le nom donnée (prénom ou nom de famille)
    @classmethod
    def filter_customers(cls, search=None):
        conn = cls.get_db()
        cursor = conn.cursor()
        
        query = "SELECT * FROM customers"
        params = []

        if search:
            query += " WHERE first_name LIKE ? OR last_name LIKE ?"
            params = [f"%{search}%", f"%{search}%"]

        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        return rows

class Orders(BaseModel):
    def __init__(self, customer_id, product_id, quantity):
        super().__init__()
        self.customer_id = customer_id
        self.product_id = product_id
        self.quantity = quantity

    # prendre toutes les commandes en utilisant un join avec la table customers et produits (clé étrangère commune)
    @classmethod
    def get_all(cls):
        conn = cls.get_db()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT 
                o.id,
                o.customer_id,
                o.product_id,
                o.quantity,
                o.date_added,
                c.first_name,
                c.last_name,
                p.name
            FROM orders o
            JOIN customers c ON o.customer_id = c.id
            JOIN products p ON o.product_id = p.id
            ORDER BY o.date_added DESC
        ''')
        rows = cursor.fetchall()
        conn.close()
        return rows
    
    # prendre la commande par id en utilisant un join avec la table customers et produits (clé étrangère commune)
    @classmethod
    def get_by_id(cls, id):
        conn = cls.get_db()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT o.*, c.first_name, c.last_name, p.name
            FROM orders o
            JOIN customers c ON o.customer_id = c.id
            JOIN products p ON o.product_id = p.id
            WHERE o.id = ?
        ''', (id,))
        order = cursor.fetchone()
        conn.close()
        return order
    
    # sauvegarder la commande dans la table orders (tout en prenant compte des foreign key qui font référence à)
    def save(self):
        conn = self.get_db()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                date_added TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (customer_id) REFERENCES customers (id),
                FOREIGN KEY (product_id) REFERENCES products (id)
            )
        ''')
        cursor.execute('''
            INSERT INTO orders (customer_id, product_id, quantity)
            VALUES (?, ?, ?)
        ''', (self.customer_id, self.product_id, self.quantity))
        conn.commit()
        conn.close()

    # méthode statique pour effacer la commande selon l'id fournit
    @staticmethod
    def delete(id):
        conn = BaseModel.get_db()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM orders WHERE id = ?', (id,))
        conn.commit()
        conn.close()

    # filtrer les commandes dans la table html en utilisant une requête qui prend le first name et le last name du customer pour rechercher les commandes associées
    # à ce dernier en faisant un join entre les tables
    @classmethod
    def filter_orders(cls, search=None):
        conn = cls.get_db()
        cursor = conn.cursor()
        
        query = '''
            SELECT 
                o.id,
                o.customer_id,
                o.product_id,
                o.quantity,
                o.date_added,
                c.first_name,
                c.last_name,
                p.name
            FROM orders o
            JOIN customers c ON o.customer_id = c.id
            JOIN products p ON o.product_id = p.id
        '''
        params = []

        if search:
            query += " WHERE c.first_name LIKE ? OR c.last_name LIKE ?"
            params = [f"%{search}%", f"%{search}%"]

        query += " ORDER BY o.date_added DESC"
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        return rows