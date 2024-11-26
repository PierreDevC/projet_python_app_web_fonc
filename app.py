# Fichier : app.py
# Projet : Application Web Fonctionelle
# Auteurs : Pierre-Sylvestre Cypré, Aboubacar Sidiki Doumbouya
# Date : 9 Novembre 2024
# Objectif et description : Utilisation des classes créees dans models.py pour créer l'instance de classes et utiliser leurs propriétés et méthodes
# Utiliser 
# Le décorateur @loginrequired s'applique à pratiquement toutes les routes et permettra à l'application de savoir si l'utilisateur est bel et bien connecté

import os
from flask import Flask,render_template, request, url_for, redirect, send_file, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
import sqlite3
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import logging
from functools import wraps
import pandas as pd
from models import Products, Customers, Orders
import database_script

app = Flask(__name__)

# chemin absolu du répertoire
basedir = os.path.abspath(os.path.dirname(__file__))
# configuration de la base de données sql pour les utilisateurs
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# clé secrète pour la base de données
app.config['SECRET_KEY'] = 'thisisasecretkey'

# intialize la db pour intéragic avec la base de données et également initialize Bcrypt
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# fonction utilisant un décorateur pour prendre un objet user de la base de données avec leur Id pour utiliser dans Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

# formulaire pour créer un nouveau compte
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
            
# formulaire pour se connecter
class LoginForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField('Se connecter')

# page initale (la première page que le visiteur/utilisateur verra)
@app.route('/')
def home():
    return render_template('home.html')

# route pour valider le formulaire de connexion, voir si le mot de passe hash est correspondant à celui de l'utilisateur (encrypter), et authentifier l'utilisateur 
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

# route pour la page principale après avoir été loggé
@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    products = c.execute('SELECT * FROM products LIMIT 5').fetchall()
    customers = c.execute('SELECT * FROM customers LIMIT 5').fetchall()
    conn.close()
    return render_template('dashboard.html', products=products, customers=customers, user=current_user)

# route pour se déconnecter
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# route pour créer un nouvel utilisateur, hasher son mot de passe dans la base de données
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

# route qui donne la liste de tous les produits
@app.route('/product_list')
@login_required
def product_list():
    rows = Products.get_all()
    return render_template("product_list.html", rows=rows, user=current_user)

# route pour ajouter un produit en utilisant les valeurs du formulaire bootstrap
@app.route('/add_product', methods=['POST', 'GET'])
def add_product():
    if request.method == 'POST':
        try:
            new_product = Products(
                name=request.form['product_name'],
                type=request.form.get('product_type'),
                category=request.form['product_category'],
                brand=request.form['product_brand'],
                price=float(request.form['product_price']),
                stock=int(request.form['product_stock']),
                description=request.form['product_desc']
            )
            new_product.save()
            flash('Le produit a été ajouté avec succès!', 'success')
        except Exception as e:
            flash(f'Il y a eu une erreur lors de l\'ajout du produit : {e}', 'danger')
        return redirect(url_for('product_list'))

# route pour mettre à jour un produit en utilisant les valeurs du formulaire bootstrap
@app.route('/update_product', methods=['POST'])
@login_required
def update_product():
    if request.method == 'POST':
        try:
            product_data = {
                'name': request.form['product_name'],
                'type': request.form['modify_product_type'],
                'category': request.form['modify_product_category'],
                'brand': request.form['modify_product_brand'],
                'price': float(request.form['product_price']),
                'stock': int(request.form['product_stock']),
                'description': request.form['product_desc']
            }
            Products.update(request.form['product_id'], product_data)
            flash('Product successfully updated!', 'success')
        except Exception as e:
            flash(f'Error updating product: {str(e)}', 'danger')
        return redirect(url_for('product_list'))

# route pour supprimer un produit. prend le id sélectionné en checkbox, parcours la liste de product_ids et efface ceux qui sont sélectionnés
@app.route('/delete_product', methods=['POST'])
def delete_product():
    if request.method == 'POST':
        try:
            product_ids = request.form.getlist('product_ids')
            if not product_ids:
                flash('Pas de produit sélectionné à supprimer.', 'danger')
            else:
                for product_id in product_ids:
                    Products.delete(product_id)
                flash(f'{len(product_ids)} produits supprimé(s) avec succès.', 'success')
        except Exception as e:
            flash(f'Erreur lors de la suppression du produit(s): {str(e)}', 'danger')
        return redirect(url_for('product_list'))

# route pour filtrer les produits en prenant (si présent) les arguments sélectionnées dans le formulaire de filtrage et fait la requête sql dans la classe Produit
@app.route('/filter_products', methods=['GET'])
@login_required
def filter_products():
    type = request.args.get('type')
    category = request.args.get('category')
    brand = request.args.get('brand')
    search = request.args.get('search')
    
    rows = Products.filter_products(type, category, brand, search)
    return render_template("product_list.html", rows=rows)

# génère la liste de tous les clients dans la table html de la page customer_list.html
@app.route('/customer_list')
@login_required
def customer_list():
    rows = Customers.get_all()
    return render_template("customer_list.html", rows=rows, user=current_user)

# ajoute un client basé sur les informations entrées dans le modal bootstrap et le sauvegarde
@app.route('/add_customer', methods=['POST', 'GET'])
@login_required
def add_customer():
    if request.method == 'POST':
        try:
            new_customer = Customers(
                first_name=request.form['first_name'],
                last_name=request.form['last_name'],
                email=request.form['email']
            )
            new_customer.save()
            flash('Le client a été ajouté avec succès!', 'success')
        except Exception as e:
            flash(f'Il y a eu une erreur lors de l\'ajout du client : {e}', 'danger')
        return redirect(url_for('customer_list'))

# met à jour les informations d'un client en utilisant les nouvelles informations entrées dans le modal bootstrap
@app.route('/update_customer', methods=['POST'])
@login_required
def update_customer():
    if request.method == 'POST':
        try:
            customer_data = {
                'first_name': request.form['first_name'],
                'last_name': request.form['last_name'],
                'email': request.form['email']
            }
            Customers.update(request.form['id'], customer_data)
            flash('Le client a été modifié avec succès!', 'success')
        except Exception as e:
            flash(f'Erreur lors de la modification du client: {str(e)}', 'danger')
        return redirect(url_for('customer_list'))

# route pour supprimer un client. prend le id sélectionné en checkbox, parcours la liste de customer_ids et efface ceux qui sont sélectionnés
@app.route('/delete_selected_customer', methods=['POST'])
@login_required
def delete_selected_customer():
    if request.method == 'POST':
        try:
            customer_ids = request.form.getlist('customer_ids')
            if not customer_ids:
                flash('Pas de client sélectionné à effacer.', 'danger')
            else:
                for customer_id in customer_ids:
                    Customers.delete(customer_id)
                flash(f'{len(customer_ids)} clients supprimé(s) avec succès.', 'success')
        except Exception as e:
            flash(f'Erreur lors de la suppression du client(s): {str(e)}', 'danger')
        return redirect(url_for('customer_list'))

# filtre les clients par leurs prénoms et noms, récupère le paramètre de recherche search dans l'URL, appelle la méthode filtrer_customers
@app.route('/filter_customers', methods=['GET'])
@login_required
def filter_customers():
    search = request.args.get('search')
    rows = Customers.filter_customers(search)
    return render_template("customer_list.html", rows=rows)

# montre toutes les commandes en cours
# les produits et les customers seront affichés dans le modal lors de la sélection 
@app.route('/order_list')
@login_required
def order_list():
    orders = Orders.get_all()
    customers = Customers.get_all()
    products = Products.filter_products()  # prendre tous les produits avec un stock > 0
    return render_template("order_list.html", orders=orders, customers=customers, products=products)

# ajoute une nouvelle commande en prenant le id du produit spécifié, la quantité, 
# si la quantité du produit est en dessous de la quantité demandée, afficher un message d'erreur
# sinon créer la commande avec le customer_id, le product_id et la quantité et sauvegarder grâce à la méthode de la classe orders
@app.route('/add_order', methods=['POST'])
@login_required
def add_order():
    try:
        product = Products.get_by_id(request.form['product_id'])
        quantity = int(request.form['quantity'])
        
        if product['stock'] < quantity:
            flash('Stock insuffisant', 'error')
            return redirect(url_for('order_list'))
        
        new_order = Orders(
            customer_id=request.form['customer_id'],
            product_id=request.form['product_id'],
            quantity=quantity
        )
        new_order.save()
        
        Products.update_stock(request.form['product_id'], -quantity)
        flash('Commande ajoutée avec succès', 'success')
    except Exception as e:
        flash(f'Erreur lors de l\'ajout de la commande: {str(e)}', 'error')
    return redirect(url_for('order_list'))

# supprime la commande selon l'id fourni
@app.route('/delete_order/<int:order_id>', methods=['POST'])
@login_required
def delete_order(order_id):
    try:
        order = Orders.get_by_id(order_id)
        if order:
            product = Products.get_by_id(order['product_id'])
            if product:
                Products.update_stock(order['product_id'], order['quantity'])
            Orders.delete(order_id)
            flash('Commande supprimée avec succès', 'success')
        else:
            flash('Commande non trouvée', 'error')
    except Exception as e:
        flash(f'Erreur lors de la suppression de la commande: {str(e)}', 'error')
    return redirect(url_for('order_list'))

# filtre les ordres selon la recherche (input) dans la barre de recherche du collapse Bootstrap
@app.route('/filter_orders', methods=['GET'])
@login_required
def filter_orders():
    search = request.args.get('search')
    orders = Orders.filter_orders(search)
    return render_template("order_list.html", orders=orders)


# Graphiques (Données analytiques)
def generate_pie_chart():
    # Connexion à la base de données SQLite 'inventory.db'
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()

    # Exécution d'une requête SQL pour récupérer le nombre de produits par marque
    # La requête regroupe les produits par marque, compte le nombre de produits pour chaque marque
    cursor.execute('SELECT brand, COUNT(*) FROM products GROUP BY brand')
    rows = cursor.fetchall()

    # Extraction des marques et des comptes de produits à partir des résultats de la requête
    brands = [row[0] for row in rows]  # marques
    counts = [row[1] for row in rows]  # comptes de produits

    # Création d'un graphique en camembert à l'aide de matplotlib
    plt.pie(counts, labels=brands, autopct='%1.1f%%')
    plt.axis('equal')
    plt.title('Part de marché des produits par marque')

    # Sauvegarde du graphique dans un fichier nommé 'product_share.png' dans le répertoire 'static'
    plt.savefig('static/product_share.png', transparent=False)
    plt.close()

def generate_category_bar_chart():
    # Connexion à la base de données SQLite 'inventory.db'
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()

    # Exécution d'une requête SQL pour récupérer les 5 catégories avec le plus de produits
    # La requête regroupe les produits par catégorie, compte le nombre de produits dans chaque catégorie,
    # et trie les résultats par ordre décroissant selon le nombre de produits
    cursor.execute('SELECT category, COUNT(*) FROM products GROUP BY category ORDER BY COUNT(*) DESC LIMIT 5')
    rows = cursor.fetchall()

    # Extraction des noms de catégories et des comptes de produits à partir des résultats de la requête
    categories = [row[0] for row in rows]  # noms de catégories
    counts = [row[1] for row in rows]  # comptes de produits

    # Création d'un graphique à barres à l'aide de matplotlib
    plt.bar(categories, counts)
    plt.xlabel('Catégorie')  # étiquette de l'axe des x
    plt.ylabel('Nombre de produits')  # étiquette de l'axe des y
    plt.title('Top 5 catégories par nombre de produits')  # titre du graphique

    # Sauvegarde du graphique dans un fichier nommé 'category_bar_chart.png' dans le répertoire 'static'
    plt.savefig('static/category_bar_chart.png', transparent=False)
    plt.close()  # fermeture du graphique pour libérer les ressources

def generate_order_quantity_histogram():
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()

    # Prendre les valeurs de quantité de la table orders
    cursor.execute('SELECT quantity FROM orders')
    rows = cursor.fetchall()

    # Extraire les quantité dans une liste
    quantities = [row[0] for row in rows]

    # Création de l'histogramme (couleurs, valeurs x,y et titre)
    plt.hist(quantities, bins=10, color='blue', edgecolor='black')
    plt.xlabel('Order Quantity')
    plt.ylabel('Frequency')
    plt.title('Distribution of Order Quantities')

    # Sauvegarder en tant qu'image
    plt.savefig('static/order_quantity_histogram.png', transparent=False)
    plt.close()

    conn.close()

# éxecution des graphiques dans la page html
@app.route('/analytics')
@login_required
def product_share():
    generate_pie_chart()  
    generate_category_bar_chart()
    generate_order_quantity_histogram()
    return render_template('analytics.html')

# décorateur python qui enregistre les actions des utilisateurs en enregistrant leur identifiant et le nom de la fonction en cours
logging.basicConfig(filename='user_actions.log', level=logging.INFO)

def log_action(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user_id = request.cookies.get('user_id')
        action = func.__name__
        logging.info(f"User ID: {user_id}, Action: {action}")
        return func(*args, **kwargs)
    return wrapper



if __name__ == '__main__':
    app.run(debug=True)
