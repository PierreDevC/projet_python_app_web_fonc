class User:
    # constructeur utilisateur
    def __init__(self, id, username, email, password, role):
        self.id = id
        self.username = username
        self.email = email
        self.password = password #hash le mot de passe
        self.role = role

    # méthodes et fonctions de l'utilisateur

    def get_role(self):
        return self.role
    
    def is_admin(self):
        return self.role == 'admin'
    
    def is_registered(self):
        return self.role == 'registered'
    
    def is_visitor(self):
        return self.role == 'visitor'
    
    def update_profile(self, username=None, email=None):
        if username:
            self.username = username
        if email:
            self.email = email

    # Retourner l'info de l'utilisateur en tant que string
    def __str__(self):
        return f"User(id={self.id}, username={self.username}, email={self.email}, role={self.role})"
    