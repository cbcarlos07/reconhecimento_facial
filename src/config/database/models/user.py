#src/config/database/models/user.py
from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)

    def __repr__(self):
        return f"User('{self.name}', {self.username}', '{self.email}')"
    
    def to_dict(self):
        """Converte o objeto User em um dicionário."""
        return {
            'id': self.id,
            'name': self.name,
            'username': self.username,
            'email': self.email
            # Note que não incluímos 'password' por segurança
        }