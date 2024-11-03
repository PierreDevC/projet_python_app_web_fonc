import sqlite3

conn = sqlite3.connect('database/database.db')
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS produits
            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
            nom TEXT NOT NULL,
            categorie TEXT NOT NULL,
            marque TEXT NOT NULL,
            modele TEXT NOT NULL,
            prix REAL NOT NULL,
            description TEXT,
            stock INTEGER NOT NULL,
            date_ajout DATE DEFAULT CURRENT_DATE)''')
conn.commit()

cur.close()
conn.close()