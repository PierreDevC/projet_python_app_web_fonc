import sqlite3

with sqlite3.connect('produits.db') as conn:
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
    cur.execute('DELETE FROM produits WHERE nom = MacBook Air M2')
    conn.commit()

    