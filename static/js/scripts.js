/** Fichier scripts.js
 * Projet : Application Web Fonctionnelle
 * Auteurs : Pierre-Sylvestre Cypré, Aboubacar Sidiki Doumbouya
 * Date : 20 Novembre 2024
 * Objectif et description : Javascript perméttant de cocher des cases, gérer les messages de confirmation, 
 * populer les formulaires bootstrap pour la modification
 * **/




// Fermeture automatique des messages Flash
  document.addEventListener('DOMContentLoaded', function() {
      const alerts = document.querySelectorAll('.alert');
      alerts.forEach(alert => {
          // Fermer le message après 5 secondes
          setTimeout(() => {
              alert.classList.add('fade-out');
              setTimeout(() => {
                  alert.remove();
              }, 500);
          }, 5000);

          // Fermeture manuelle
          const closeButton = alert.querySelector('.btn-close');
          if (closeButton) {
              closeButton.addEventListener('click', () => {
                  alert.classList.add('fade-out');
                  setTimeout(() => {
                      alert.remove();
                  }, 500);
              });
          }
      });
  });


  // Code pour la page Products
  function toggleDeleteProductButton() {
    const checkboxes = document.querySelectorAll('input[name="product_ids"]:checked');
    const deleteBtn = document.getElementById('deleteBtn');
    
    if (checkboxes.length > 0) {
        deleteBtn.style.display = 'inline-block';
    } else {
        deleteBtn.style.display = 'none';
    }
}

function selectAllCheckboxesProducts() {
    var selectAllCheckbox = document.getElementById('selectAll');
    var checkboxes = document.getElementsByName('product_ids');

    if (selectAllCheckbox.checked) {
        for (var i = 0; i < checkboxes.length; i++) {
            checkboxes[i].checked = true;
        }
    } else {
        for (var i = 0; i < checkboxes.length; i++) {
            checkboxes[i].checked = false;
        }
    }
}

function populateModifyModal(button) {
    const data = button.dataset;

    document.getElementById('modify_product_id').value = data.id;
    document.getElementById('modify_product_name').value = data.name;
    document.querySelector(`input[name="modify_product_type"][value="${data.type}"]`).checked = true;
    document.querySelector(`input[name="modify_product_category"][value="${data.category}"]`).checked = true;
    document.querySelector('select[name="modify_product_brand"]').value = data.brand;
    document.getElementById('modify_product_price').value = data.price;
    document.getElementById('modify_product_stock').value = data.stock;
    document.getElementById('modify_product_desc').value = data.description;
}

const buttonProduct = document.querySelector('.buttons');
const collapseProduct = document.querySelector('#collapseExample');



// Code pour la page clients (Customers)
function toggleDeleteButton() {
    // Boutons checked
    const checkboxes = document.querySelectorAll('input[name="customer_ids"]:checked');
    // Bouton delete
    const deleteBtn = document.getElementById('deleteBtn');
    // Si au moins un bouton est checked, montrer le bouton
    if (checkboxes.length > 0) {
        deleteBtn.style.display = 'inline-block'; // Montrer bouton
    } else {
        deleteBtn.style.display = 'none'; // Cacher bouton
    }
}

// Sélectionner toutes les cases
function selectAllCheckboxesCustomers() {
    var selectAllCheckbox = document.getElementById('selectAll');
    var checkboxes = document.getElementsByName('customer_ids');

    if (selectAllCheckbox.checked) {
        for (var i = 0; i < checkboxes.length; i++) {
            checkboxes[i].checked = true;
        }
    } else {
        for (var i = 0; i < checkboxes.length; i++) {
            checkboxes[i].checked = false;
        }
    }
}

// Insère les données existantes dans le modl bootstrap
function populateModifyCustomer(button) {
    const data = button.dataset;
    document.getElementById('modify_customer_id').value = data.id;
    document.getElementById('modify_customer_first_name').value = data.firstName;
    document.getElementById('modify_customer_last_name').value = data.lastName;
    document.getElementById('modify_customer_email').value = data.email;
}
const buttonCustomer = document.querySelector('.buttons');
const collapseCustomer = document.querySelector('#collapseExample');


// Code pour la page Commandes (Orders)
function toggleDeleteOrderButton() {
    const checkboxes = document.querySelectorAll('input[name="order_ids"]:checked');
    const deleteBtn = document.getElementById('deleteBtn');
    
    if (checkboxes.length > 0) {
        deleteBtn.style.display = 'inline-block';
    } else {
        deleteBtn.style.display = 'none';
    }
}


// Coche toutes les cases
function selectAllCheckboxesOrders() {
    var selectAllCheckbox = document.getElementById('selectAll');
    var checkboxes = document.getElementsByName('order_ids');
    
    for (var i = 0; i < checkboxes.length; i++) {
        checkboxes[i].checked = selectAllCheckbox.checked;
    }
}


// Met à jour la quantité maximale que l'utilisateur peut saisir dans le champ du formulaire quantité en fonction du stock
function updateQuantityMax() {
    const productSelect = document.getElementById('product_id');
    const quantityInput = document.getElementById('quantity');
    const selectedOption = productSelect.options[productSelect.selectedIndex];
    const maxStock = selectedOption.getAttribute('data-stock');
    
    quantityInput.max = maxStock;
    quantityInput.value = Math.min(quantityInput.value, maxStock);
    document.getElementById('available_stock').textContent = maxStock;
}