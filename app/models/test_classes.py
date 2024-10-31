# Import the Produit class
from produits import *

# Create a new Produit object
produit1 = Produit("iPhone 13", "téléphone", "Apple", "A1234", 999.99, "Smartphone haut de gamme", 50)

# Create the produits table in the database
Produit.creer_table()

# Add the produit to the database
produit1.ajouter_produit()

# Get all produits from the database
produits = Produit.obtenir_produits()
for produit in produits:
    print(produit)

# Update a produit in the database
produit1.mettre_a_jour_produit(1, description="Nouveau smartphone Apple")

# Delete a produit from the database
Produit.supprimer_produit(1)