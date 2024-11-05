from flask import Flask,render_template, request

from products import Products
from users import User

import sqlite3 as sql

app = Flask(__name__)

@app.route('/')
def home():
        return render_template('home.html')

@app.route('/enternew')
def new_product():
      return render_template('products.html')

@app.route('/addrec',methods=['POST', 'GET'])
def addrec():
      if request.method == 'POST':
            try:
                product_name = request.form['product_name']
                product_type = request.form['product_type']
                product_category = request.form['product_category']
                product_brand = request.form['product_brand']
                product_price = request.form['product_price']
                product_stock = request.form['product_stock']
                product_desc = request.form['product_desc']
                

                # ajouter un produit en utilisant la clase produits

                with sql.connect('inventory.db') as conn:
                        cursor = conn.cursor()
                        cursor.execute('''
                        CREATE TABLE IF NOT EXISTS products (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        type TEXT NOT NULL,
                        category TEXT NOT NULL,
                        brand TEXT NOT NULL,
                        price REAL NOT NULL,
                        stock INTEGER,
                        description TEXT,
                        date_added TEXT NOT NULL DEFAULT CURRENT_DATE
                        )
                        ''')

                        cur.execute(f"INSERT INTO products {product_name}, {product_type}, {product_category}, {product_brand}")

                        product_obj = Products("MacBook Pro", "Laptop", "Productivity", "Apple", 1999.99, 50, "High-performance laptop for professionals")


                with sql.connect('inventory.db') as conn:
                        cur = conn.cursor()
                        cur.execute("INSERT INTO students (name, addr, city, pin) VALUES (?,?,?,?)")

                        msg = "Record successfully added"

            except:
                conn.rollback()
                msg = "There was an error inserting the product"
            
            finally:
                conn.close()
                return render_template("result.html", msg=msg)
                



if __name__ == '__main__':
    app.run(debug=True)

