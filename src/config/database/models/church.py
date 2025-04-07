#src/config/database/models/service.py
from . import db

class Church(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)

    def __repr__(self):
        return f"Service('{self.name}'"
    
    def to_dict(self):
        
        return {
            'id': self.id,
            'name': self.name
        }