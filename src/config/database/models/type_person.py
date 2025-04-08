#src/config/database/models/member.py
from . import db

class TypePerson(db.Model):
    __tablename__ = 'type_person'  # Define o nome da tabela

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    
    def __repr__(self):
        return f"Type Person('{self.name}'"
    
    def to_dict(self):
        
        return {
            'id': self.id,
            'name': self.name
        }