import sqlite3

conn = sqlite3.connect('database/database.db')
cur = conn.cursor()

# Insertion d'un produit
cur.execute("INSERT INTO produits (nom, categorie, marque, modele, prix, description, stock) VALUES ('iPhone 15 Pro', 'téléphone', 'Apple', 'A2850', 1199.99, ' ', 50)")
cur.execute("INSERT INTO produits (nom, categorie, marque, modele, prix, description, stock) VALUES ('MacBook Air M2', 'ordinateur portable', 'Apple', 'A2681', 1299.99, 'Ordinateur portable léger avec puce M2', 30)")

# Affichage de tous les éléments de la table produits
cur.execute("SELECT * FROM produits")
rows = cur.fetchall()
for row in rows:
    print(row)
    
# Mise à jour du produit (ajout d'une description)
cur.execute("UPDATE produits SET description = 'Le dernier iPhone avec puce A17 Pro' WHERE nom = 'Iphone 15 Pro'")
conn.commit()

# Supprimer un produit
cur.execute("DELETE FROM produits WHERE nom = 'MacBook Air M2'")
conn.commit()


# Création de tuples contenant les informations des produits
produits = (
    ('Samsung Galaxy S24', 'téléphone', 'Samsung', 'SM-S921B', 999.99, 'Smartphone haut de gamme avec IA intégrée', 40),
    ('Sony PlayStation 5', 'console de jeu', 'Sony', 'CFI-1200', 499.99, 'Console de jeu nouvelle génération', 25),
    ('Dell XPS 15', 'ordinateur portable', 'Dell', '9530', 1799.99, 'Ordinateur portable puissant pour les professionnels', 20),
    ('iPad Air', 'tablette', 'Apple', 'A2588', 649.99, 'Tablette légère et performante', 35),
    ('Canon EOS R6', 'appareil photo', 'Canon', '4082C002', 2499.99, 'Appareil photo hybride plein format', 15),
    ('Bose QuietComfort 45', 'casque audio', 'Bose', '866724-0100', 329.99, 'Casque à réduction de bruit active', 50),
    ('LG OLED C3', 'téléviseur', 'LG', 'OLED65C3PUA', 2499.99, 'Téléviseur OLED 4K 65 pouces', 10),
    ('Dyson V15 Detect', 'aspirateur', 'Dyson', '368734-01', 699.99, 'Aspirateur sans fil avec détection laser de la poussière', 30)
)

# Insertion des produits
cur.executemany("INSERT INTO produits (nom, categorie, marque, modele, prix, description, stock) VALUES (?, ?, ?, ?, ?, ?, ?)", produits)





conn.commit()
conn.close()