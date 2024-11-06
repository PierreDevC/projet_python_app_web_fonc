from flask import Flask,render_template, request

from products import Products
from users import User

import sqlite3

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
                name = request.form['product_name']
                type = request.form['product_type']
                category = request.form['product_category']
                brand = request.form['product_brand']
                price = request.form['product_price']
                stock = request.form['product_stock']
                desc = request.form['product_desc']
                
                # Instance de l'objet de produit
                new_product = Products(name, type, category, brand, price, stock, desc)

                with sqlite3.connect('inventory.db') as conn:
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

                        # éviter l'injection sql en utilisant des requêtes paramètrées
                        sql = "INSERT INTO products (name, type, category, brand, price, stock, description) VALUES (?, ?, ?, ?, ?, ?, ?)"
                        args = (new_product.name, new_product.type, new_product.category, new_product.brand, new_product.price, new_product.stock, new_product.description)
                        cursor = conn.execute(sql, args)
                        conn.commit()
                        msg = "Product successfully added"

                        # utiliser add_product

            except:
                conn.rollback()
                msg = "There was an error inserting the product"
            
            finally:
                conn.close()
                return render_template("result.html", msg=msg)
                
                
@app.route('/list')
def list():
        with sqlite3.connect('inventory.db') as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute('''SELECT * from products''')
                rows = cursor.fetchall()
                return render_template("list.html",rows=rows)

                

          


        


if __name__ == '__main__':
    app.run(debug=True)

