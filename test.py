import sqlite3

conn = sqlite3.connect('inventory.db')
cursor = conn.cursor()

cursor.execute('''DROP TABLE products ''')

conn.commit()
conn.close()