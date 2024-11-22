
import os
from flask import Flask,render_template, request, url_for, redirect, send_file, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
from models import Products
from models import Customers
import sqlite3
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

app = Flask(__name__)

# Authentication logic
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'thisisasecretkey'

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
    submit = SubmitField('Créer le compte')

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            flash('Ce nom d\'utilisateur existe déja.', 'danger')
            raise ValidationError(
                'Ce nom d\'utilisateur existe déja.')
            

class LoginForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField('Se connecter')

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
                flash('Connexion réussie!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Mot de passe invalide. Veuillez réessayer.', 'danger')
        else:
            flash("Nom d'utilisateur ou mot de passe incorrect.", 'danger')
            return redirect(url_for('login'))
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

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

# Product Routes
@app.route('/add_product',methods=['POST', 'GET'])
def add_product():
    if request.method == 'POST':
        try:
            name = request.form['product_name']
            type = request.form.get('product_type')
            category = request.form['product_category']
            brand = request.form['product_brand']
            price = request.form['product_price']
            stock = request.form['product_stock']
            desc = request.form['product_desc'] 
            
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

                sql = "INSERT INTO products (name, type, category, brand, price, stock, description) VALUES (?, ?, ?, ?, ?, ?, ?)"
                args = (new_product.name, new_product.type, new_product.category, new_product.brand, new_product.price, new_product.stock, new_product.description)
                cursor = conn.execute(sql, args)
                conn.commit()
                flash(f'Le produit a été ajouté avec succès!', 'success')

        except Exception as e:
            conn.rollback()
            flash(f'Il y a eu une erreur lors de l\'ajout du produit : {e}', 'danger')
        
        finally:
            conn.close()
            return redirect(url_for('product_list', user=current_user))

@app.route('/update_product', methods=['POST'])
@login_required
def update_product():
    if request.method == 'POST':
        try:
            product_id = request.form['product_id']
            name = request.form['product_name']
            product_type = request.form['modify_product_type']
            category = request.form['modify_product_category']
            brand = request.form['modify_product_brand']
            price = request.form['product_price']
            stock = request.form['product_stock']
            description = request.form['product_desc']
            
            with sqlite3.connect('inventory.db') as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE products 
                    SET name=?, type=?, category=?, brand=?, price=?, stock=?, description=?
                    WHERE id=?
                ''', (name, product_type, category, brand, price, stock, description, product_id))
                conn.commit()
                flash('Product successfully updated!', 'success')
        except Exception as e:
            conn.rollback()
            flash(f'Error updating product: {str(e)}', 'danger')
        finally:
            return redirect(url_for('product_list', user=current_user))

@app.route('/delete_product', methods=['POST'])
def delete_product():
    if request.method == 'POST':
        try:
            product_ids = request.form.getlist('product_ids')
            
            if not product_ids:
                flash('Pas de produit sélectionné à supprimer. Veuillez sélectionner au moins un produit', 'danger')
            else:
                with sqlite3.connect('inventory.db') as conn:
                    cursor = conn.cursor()
                    
                    sql = "DELETE FROM products WHERE id IN ({})".format(','.join('?' for _ in product_ids))
                    cursor.execute(sql, product_ids)
                    conn.commit()
                    
                    flash(f'{len(product_ids)} produits supprimé(s) avec succès.', 'success')
        
        except Exception as e:
            conn.rollback()
            flash(f'Erreur lors de la suppression du produit(s): {str(e)}', 'danger')
        
        finally:
            conn.close()
            return redirect(url_for('product_list'))

@app.route('/product_list')
@login_required
def product_list():
    with sqlite3.connect('inventory.db') as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('''SELECT * from products''')
        rows = cursor.fetchall()
        return render_template("product_list.html",rows=rows, user=current_user)
    

@app.route('/filter_products', methods=['GET'])
@login_required
def filter_products():
    type = request.args.get('type')
    category = request.args.get('category')
    brand = request.args.get('brand')
    search = request.args.get('search')

    query = "SELECT * FROM products"

    conditions = []
    params = ()

    if type:
        conditions.append("type = ?")
        params += (type,)

    if category:
        conditions.append("category = ?")
        params += (category,)

    if brand:
        conditions.append("brand = ?")
        params += (brand,)

    if search:
        conditions.append("name LIKE ?")
        params += (f"%{search}%",)

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    with sqlite3.connect('inventory.db') as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        return render_template("product_list.html", rows=rows)

# Customers routes
@app.route('/customer_list')
@login_required
def customer_list():
    with sqlite3.connect('inventory.db') as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('''SELECT * from customers''')
        rows = cursor.fetchall()
        return render_template("customer_list.html", rows=rows, user=current_user)

@app.route('/add_customer', methods=['POST', 'GET'])
def add_customer():
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
                flash(f'Le client a été ajouté avec succès!', 'success')

        except Exception as e:
            conn.rollback()
            flash(f'Il y a eu une erreur lors de l\'ajout du client : {e}', 'danger')

        finally:
            conn.close()
            return redirect(url_for('customer_list'))


@app.route('/update_customer', methods=['POST'])
@login_required
def update_customer():
    if request.method == 'POST':
        try:
            customer_id = request.form['id']
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            email = request.form['email']
            
            with sqlite3.connect('inventory.db') as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE customers
                    SET first_name=?, last_name=?, email=?
                    WHERE id=?
                ''', (first_name, last_name, email, customer_id))
                conn.commit()
                flash('Le client a été modifié avec succès!', 'success')
        except Exception as e:
            conn.rollback()
            flash(f'Erreur lors de la modification du client: {str(e)}', 'danger')
        finally:
            return redirect(url_for('customer_list', user=current_user))


@app.route('/delete_selected_customer', methods=['POST'])
@login_required
def delete_selected_customer():
    if request.method == 'POST':
        try:
            customer_ids = request.form.getlist('customer_ids', type=int)

            if not customer_ids:
                flash('Pas de client sélectionné à effacer. Veuillez sélectionner au moins un client', 'danger')
            else:
                with sqlite3.connect('inventory.db') as conn:
                    cursor = conn.cursor()
                    sql = "DELETE FROM customers WHERE id IN (%s)" % ','.join('?' for _ in customer_ids)
                    cursor.execute(sql, customer_ids)
                    conn.commit()
                    flash(f'{len(customer_ids)} clients supprimé(s) avec succès.', 'success')

        except sqlite3.Error as e:
            conn.rollback()
            flash(f'Erreur lors de la suppression du client(s): {str(e)}', 'danger')

        finally:
            conn.close()
            return redirect(url_for('customer_list'))


# en progression...
@app.route('/filter_customers', methods=['GET'])
@login_required
def filter_customers():
    search = request.args.get('search')

    query = "SELECT * FROM customers"
    conditions = []
    params = ()

    if search:
        conditions.append("(first_name LIKE ? OR last_name LIKE ?)")
        params += (f"%{search}%", f"%{search}%")

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    try:
        with sqlite3.connect('inventory.db') as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            return render_template("customer_list.html", rows=rows)
    except sqlite3.Error as e:
        flash(f"Error filtering customers: {str(e)}", 'error')
        return redirect(url_for('customer_list'))




# Order routes
@app.route('/order_list')
@login_required
def order_list():
    with sqlite3.connect('inventory.db') as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('''SELECT o.id, o.customer_id, o.product_id, o.quantity, 
                          c.first_name, c.last_name, 
                          p.name, p.stock
                          FROM orders o 
                          JOIN customers c ON o.customer_id = c.id 
                          JOIN products p ON o.product_id = p.id''')
        orders = cursor.fetchall()
        return render_template("order_list.html", orders=orders)
    
@app.route('/add_order', methods=['POST'])
@login_required
def add_order():
    try:
        customer_id = request.form['customer_id']
        product_id = request.form['product_id']
        quantity = int(request.form['quantity'])

        with sqlite3.connect('inventory.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT stock FROM products WHERE id=?', (product_id,))
            product_stock = cursor.fetchone()[0]
            if product_stock < quantity:
                flash('Pas assez de stock disponible', 'error')
                return redirect(url_for('order_list'))

            cursor.execute('INSERT INTO orders (customer_id, product_id, quantity) VALUES (?, ?, ?)', (customer_id, product_id, quantity))
            cursor.execute('UPDATE products SET stock=stock-? WHERE id=?', (quantity, product_id))
            conn.commit()

            flash('Commande ajoutée avec succès', 'success')
    except Exception as e:
        flash(f'Error adding order: {str(e)}', 'error')

    return redirect(url_for('order_list'))


@app.route('/delete_order/<int:order_id>', methods=['POST'])
@login_required
def delete_order(order_id):
    if request.method == 'POST':
        try:
            with sqlite3.connect('inventory.db') as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT product_id, quantity FROM orders WHERE id=?', (order_id,))
                order_data = cursor.fetchone()
                if order_data is None:
                    flash('La commande n\'a pas été trouvée', 'success')
                else:
                    product_id, quantity = order_data
                    cursor.execute('UPDATE products SET stock=stock+? WHERE id=?', (quantity, product_id))
                    cursor.execute('DELETE FROM orders WHERE id=?', (order_id,))
                    conn.commit()
                    flash('Commande supprimée avec succès', 'success')

            return redirect(url_for('order_list'))

        except Exception as e:
            flash(f'Erreur lors de la suppression de la commande: {str(e)}')
            return redirect(url_for('order_list'))


# Analytics routes
def generate_pie_chart():
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()

    cursor.execute('SELECT brand, COUNT(*) FROM products GROUP BY brand')
    rows = cursor.fetchall()

    brands = [row[0] for row in rows]
    counts = [row[1] for row in rows]

    plt.pie(counts, labels=brands, autopct='%1.1f%%')
    plt.axis('equal')
    plt.title('Product Share by Brand')

    plt.savefig('static/product_share.png', transparent=True)
    plt.close()

def generate_category_bar_chart():
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()

    cursor.execute('SELECT category, COUNT(*) FROM products GROUP BY category ORDER BY COUNT(*) DESC LIMIT 5')
    rows = cursor.fetchall()

    categories = [row[0] for row in rows]
    counts = [row[1] for row in rows]

    plt.bar(categories, counts)
    plt.xlabel('Category')
    plt.ylabel('Number of Products')
    plt.title('Top 5 Categories by Number of Products')

    plt.savefig('static/category_bar_chart.png', transparent=True)
    plt.close()

def generate_price_histogram():
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()

    cursor.execute('SELECT price FROM products')
    rows = cursor.fetchall()

    prices = [row[0] for row in rows]

    plt.hist(prices, bins=50)
    plt.xlabel('Price')
    plt.ylabel('Frequency')
    plt.title('Distribution of Product Prices')

    plt.savefig('static/price_histogram.png', transparent=True)
    plt.close()

@app.route('/analytics')
@login_required
def product_share():
    generate_pie_chart()  
    generate_category_bar_chart()
    generate_price_histogram()
    return render_template('analytics.html')

if __name__ == '__main__':
    app.run(debug=True)
