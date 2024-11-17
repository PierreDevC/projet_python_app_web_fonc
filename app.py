import os
from flask import Flask,render_template, request, url_for, redirect, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
from models import Products
from models import Customers
import sqlite3
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


app = Flask(__name__)

# Logique d'authentification
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'thisisasecretkey' #changer le key plus tard

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

class RegisterForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Register')

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                'That username already exists. Please choose a different one.')

class LoginForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')



@app.route('/')
def home():
        return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    products = c.execute('SELECT * FROM products LIMIT 5').fetchall()
    customers = c.execute('SELECT * FROM customers LIMIT 5').fetchall()
    conn.close()

    return render_template('dashboard.html', products=products, customers=customers, user=current_user)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@ app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


# Logique de produits/customers/orders
@app.route('/enternew')
def new_product():
      return render_template('add_product.html')

@app.route('/addrec',methods=['POST', 'GET'])
def addrec():
      if request.method == 'POST':
            try:
                name = request.form['product_name']
                type = request.form.get('product_type')
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

                        # utiliser add_product...

            except:
                conn.rollback()
                msg = "There was an error inserting the product"
            
            finally:
                conn.close()
                return render_template("result.html", msg=msg)
                

'''
@app.route('/modify/<int:product_id>', methods=['GET'])
def modify_product(product_id):
    product_data = Products.get_product_by_id("inventory.db", product_id)
    if product_data:
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


@app.route('/update_product/<int:product_id>', methods=['POST'])
def update_product(product_id):
    name = request.form['name']
    product_type = request.form['type']
    category = request.form['category']
    brand = request.form['brand']
    price = request.form['price']
    stock = request.form['stock']
    description = request.form['description']
    
    updated_product = Products(name, product_type, category, brand, price, stock, description)
    updated_product.id = product_id

    updated_product.update_product("inventory.db")
    return redirect(url_for('list'))

'''
                
@app.route('/delete_selected', methods=['POST'])
def delete_selected():
    if request.method == 'POST':
        try:
            product_ids = request.form.getlist('product_ids')
            
            if not product_ids:
                msg = "No products selected for deletion."
            else:
                with sqlite3.connect('inventory.db') as conn:
                    cursor = conn.cursor()
                    
                    # Effacement dans la table
                    # Ajouter logique pour les relations étrangères
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
@login_required
def list():
        with sqlite3.connect('inventory.db') as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute('''SELECT * from products''')
                rows = cursor.fetchall()
                return render_template("product_list.html",rows=rows)

        

# Table customers
@app.route('/addcustomer', methods=['POST', 'GET'])
def addcustomer():
    if request.method == 'POST':
        try:
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            email = request.form['email']

            new_customer = Customers(first_name, last_name, email)

            with sqlite3.connect('inventory.db') as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS customers (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        first_name TEXT NOT NULL,
                        last_name TEXT NOT NULL,
                        email TEXT NOT NULL,
                        date_added TEXT NOT NULL DEFAULT CURRENT_DATE
                    )
                ''')

                sql = "INSERT INTO customers (first_name, last_name, email, date_added) VALUES (?, ?, ?, CURRENT_DATE)"
                args = (new_customer.first_name, new_customer.last_name, new_customer.email)
                cursor.execute(sql, args)
                conn.commit()
                msg = "Customer successfully added"

        except sqlite3.Error as e:
            conn.rollback()
            msg = f"There was an error inserting the customer: {e}"

        finally:
            return render_template("customer_result.html", msg=msg)
               

@app.route('/modify/<int:customer_id>', methods=['GET'])
def modify_product(customer_id):
    product_data = Products.get_product_by_id("inventory.db", customer_id)
    if product_data:
        product = {
            'id': product_data[0],
            'first_name': product_data[1],
            'last_name': product_data[2],
            'email': product_data[3],
            'date_added': product_data[4]
        }
        return render_template('modify_customer.html', product=product)
    else:
        return "Product not found", 404


@app.route('/update_product/<int:product_id>', methods=['POST'])
def update_product(product_id):
    name = request.form['name']
    product_type = request.form['type']
    category = request.form['category']
    brand = request.form['brand']
    price = request.form['price']
    stock = request.form['stock']
    description = request.form['description']
    
    updated_product = Products(name, product_type, category, brand, price, stock, description)
    updated_product.id = product_id

    updated_product.update_product("inventory.db")
    return redirect(url_for('list'))


@app.route('/delete_selected_customer', methods=['POST'])
def delete_selected_customer() -> None:
    if request.method == 'POST':
        try:
            customer_ids = request.form.getlist('customer_ids', type=int)

            if not customer_ids:
                error_message = "No customer selected for deletion"
            else:
                with sqlite3.connect('inventory.db') as conn:
                    cursor = conn.cursor()
                    sql = "DELETE FROM customers WHERE id IN (%s)" % ','.join('?' for _ in customer_ids)
                    cursor.execute(sql, customer_ids)
                    conn.commit()
                    success_message = f"{len(customer_ids)} customer(s) successfully deleted."

            return render_template('customer_result.html', message=success_message or error_message)

        except sqlite3.Error as e:
            error_message = f"There was an error deleting the customers: {str(e)}"
            return render_template('customer_result.html', message=error_message)



@app.route('/customer_list')
@login_required
def customers_list():
            with sqlite3.connect('inventory.db') as conn:
                 conn.row_factory = sqlite3.Row
                 cursor = conn.cursor()
                 cursor.execute('''SELECT * from customers''')
                 rows = cursor.fetchall()
                 return render_template("customer_list.html", rows=rows)





# Analytics

def generate_pie_chart():
    # Connect to the database
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()

    # Query the database to retrieve the brand data
    cursor.execute('SELECT brand, COUNT(*) FROM products GROUP BY brand')
    rows = cursor.fetchall()

    # Extract the brand names and counts
    brands = [row[0] for row in rows]
    counts = [row[1] for row in rows]

    # Create the pie chart
    plt.pie(counts, labels=brands, autopct='%1.1f%%')
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title('Product Share by Brand')

    # Save the plot to a file
    plt.savefig('static/product_share.png')
    plt.close()

def generate_category_bar_chart():
    # Connect to the database
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()

    # Query the database to retrieve the category data
    cursor.execute('SELECT category, COUNT(*) FROM products GROUP BY category ORDER BY COUNT(*) DESC LIMIT 5')
    rows = cursor.fetchall()

    # Extract the category names and counts
    categories = [row[0] for row in rows]
    counts = [row[1] for row in rows]

    # Create the bar chart
    plt.bar(categories, counts)
    plt.xlabel('Category')
    plt.ylabel('Number of Products')
    plt.title('Top 5 Categories by Number of Products')

    # Save the plot to a file
    plt.savefig('static/category_bar_chart.png')
    plt.close()

def generate_price_histogram():
    # Connect to the database
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()

    # Query the database to retrieve the price data
    cursor.execute('SELECT price FROM products')
    rows = cursor.fetchall()

    # Extract the price values
    prices = [row[0] for row in rows]

    # Create the histogram
    plt.hist(prices, bins=50)
    plt.xlabel('Price')
    plt.ylabel('Frequency')
    plt.title('Distribution of Product Prices')

    # Save the plot to a file
    plt.savefig('static/price_histogram.png')
    plt.close()

def generate_other_graphs():
    generate_category_bar_chart()
    generate_price_histogram()

@app.route('/product_share')
def product_share():
    generate_pie_chart()  # Update the plot
    generate_other_graphs()
    return render_template('product_share.html')

if __name__ == '__main__':

    with sqlite3.connect('inventory.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT NOT NULL,
        date_added TEXT NOT NULL DEFAULT CURRENT_DATE  
        )
        ''')

        # List of 10 products
    products = [
        ("MacBook Pro", "Laptop", "Productivity", "Apple", 1999.99, 50, "High-performance laptop for professionals"),
        ("Dell XPS 15", "Laptop", "Productivity", "Dell", 1499.99, 30, "Powerful and sleek laptop for work and entertainment"),
        ("Alienware Aurora R12", "Desktop", "Gaming", "Dell", 1799.99, 20, "High-end gaming desktop with customizable RGB lighting"),
        ("HP Envy 34", "Desktop", "Workstation", "HP", 1999.99, 15, "All-in-one desktop with a large curved display"),
        ("Lenovo ThinkPad X1 Carbon", "Laptop", "Productivity", "Lenovo", 1399.99, 40, "Ultra-light business laptop with long battery life"),
        ("ASUS ROG Zephyrus G14", "Laptop", "Gaming", "Asus", 1499.99, 25, "Compact and powerful gaming laptop"),
        ("iMac 24-inch", "Desktop", "Productivity", "Apple", 1299.99, 35, "Colorful all-in-one desktop with M1 chip"),
        ("Microsoft Surface Laptop 4", "Laptop", "Productivity", "Microsoft", 999.99, 45, "Sleek and versatile laptop with touchscreen"),
        ("Acer Predator Helios 300", "Laptop", "Gaming", "Acer", 1199.99, 30, "Popular mid-range gaming laptop"),
        ("HP Z4 G4", "Desktop", "Workstation", "HP", 2499.99, 10, "High-performance workstation for demanding tasks")
    ]

    # Connect to the database and insert products
    with sqlite3.connect('inventory.db') as conn:
        cursor = conn.cursor()
        cursor.executemany('''
        INSERT INTO products (name, type, category, brand, price, stock, description)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', products)
        conn.commit()

    print("10 products have been added to the database.")

    app.run(debug=True)


