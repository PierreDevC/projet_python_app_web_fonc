from flask import Flask,render_template, request, url_for, redirect

from models import Products

import sqlite3

app = Flask(__name__)

@app.route('/')
def home():
        return render_template('home.html')

@app.route('/enternew')
def new_product():
      return render_template('add_product.html')

@app.route('/addrec',methods=['POST', 'GET'])
def addrec():
      if request.method == 'POST':
            try:
                name = request.form['product_name']
                type = request.form.get('product_type')  # Use .get() to avoid KeyError if it's not selected
                category = request.form['product_category']
                brand = request.form['product_brand']
                price = request.form['product_price']
                stock = request.form['product_stock']
                desc = request.form['product_desc'] # textarea_content = request.form['textarea_input']
                
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
                

# Route to display the form to modify a specific product
@app.route('/modify/<int:product_id>', methods=['GET'])
def modify_product(product_id):
    # Fetch product details using Products class
    product_data = Products.get_product_by_id("inventory.db", product_id)
    if product_data:
        # Convert to dictionary format for ease of use in template
        product = {
            'id': product_data[0],
            'name': product_data[1],
            'type': product_data[2],
            'category': product_data[3],
            'brand': product_data[4],
            'price': product_data[5],
            'stock': product_data[6],
            'description': product_data[7],
            'date_added': product_data[8]
        }
        return render_template('modify_product.html', product=product)
    else:
        return "Product not found", 404


# Route to handle product updates
@app.route('/update_product/<int:product_id>', methods=['POST'])
def update_product(product_id):
    # Get updated data from the form
    name = request.form['name']
    product_type = request.form['type']
    category = request.form['category']
    brand = request.form['brand']
    price = request.form['price']
    stock = request.form['stock']
    description = request.form['description']
    
    # Create an instance with updated data and set its ID for updating
    updated_product = Products(name, product_type, category, brand, price, stock, description)
    updated_product.id = product_id  # Set product ID to update
    
    # Use the Products class to update product details
    updated_product.update_product("inventory.db")
    
    # Redirect back to product list after updating
    return redirect(url_for('list'))

                
@app.route('/delete_selected', methods=['POST'])
def delete_selected():
    if request.method == 'POST':
        try:
            # Get the list of selected product IDs
            product_ids = request.form.getlist('product_ids')
            
            if not product_ids:
                msg = "No products selected for deletion."
            else:
                with sqlite3.connect('inventory.db') as conn:
                    cursor = conn.cursor()
                    
                    # Create SQL query to delete selected products by ID
                    sql = "DELETE FROM products WHERE id IN ({})".format(','.join('?' for _ in product_ids))
                    cursor.execute(sql, product_ids)
                    conn.commit()
                    
                    msg = f"{len(product_ids)} product(s) successfully deleted."
        
        except Exception as e:
            conn.rollback()
            msg = f"There was an error deleting the products: {str(e)}"
        
        finally:
            conn.close()
            return render_template('result.html', msg=msg)

          
@app.route('/product_list')
def list():
        with sqlite3.connect('inventory.db') as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute('''SELECT * from products''')
                rows = cursor.fetchall()
                return render_template("product_list.html",rows=rows)

        
    


if __name__ == '__main__':
    app.run(debug=True)