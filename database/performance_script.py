import sqlite3

conn = sqlite3.connect('database/database.db')
cur = conn.cursor()

# Affichage plus efficace des produits (gains en performance)
cur.execute("SELECT nom, categorie, prix FROM produits")
rows = cur.fetchall()
for row in rows:
    print(row)


# Mise à jour paramétrée (gains en performance)
cur.execute("UPDATE produits SET description = ? WHERE nom = ?",
            ('Tablette fine et puissante', 'iPad Air'))
conn.commit()

# Effacement paramétré (gains en performance)
cur.execute("DELETE FROM produits WHERE nom = ?", ('Dyson V15 Detect',))
conn.commit()


conn.close()