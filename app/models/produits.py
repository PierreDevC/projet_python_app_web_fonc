import sqlite3
from datetime import datetime

class Produit:
    def __init__(self, nom, categorie, marque, modele, prix, description, stock, date_ajout=None):
        self.nom = nom
        self.categorie = categorie
        self.marque = marque
        self.modele = modele
        self.prix = prix
        self.description = description
        self.stock = stock
        self.date_ajout = date_ajout or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    
    def creer_table():
        # Création de la table produits
        with sqlite3.connect("inventaire.db") as conn:
            cursor = conn.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS produits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT,
                categorie TEXT,
                marque TEXT,
                modele TEXT,
                prix REAL,
                description TEXT,
                stock INTEGER,
                date_ajout TEXT
            )
            """)
            conn.commit()

    def ajouter_produit(self):
        # Ajout d'un nouveau produit
        with sqlite3.connect("inventaire.db") as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO produits (nom, categorie, marque, modele, prix, description, stock, date_ajout) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (self.nom, self.categorie, self.marque, self.modele, self.prix, self.description, self.stock, self.date_ajout))
            conn.commit()

    
    def obtenir_produits():
        # Consultation de la liste des produits
        with sqlite3.connect("inventaire.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM produits")
            return cursor.fetchall()

    def mettre_a_jour_produit(self, produit_id, **kwargs):
        # Mise à jour des informations d'un produit
        with sqlite3.connect("inventaire.db") as conn:
            cursor = conn.cursor()
            for key, value in kwargs.items():
                cursor.execute(f"UPDATE produits SET {key} = ? WHERE id = ?", (value, produit_id))
            conn.commit()

   
    def supprimer_produit(produit_id):
        # Suppression d'un produit
        with sqlite3.connect("inventaire.db") as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM produits WHERE id = ?", (produit_id,))
            conn.commit()
