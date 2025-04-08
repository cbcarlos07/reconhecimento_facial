#src/config/database/models/member.py
from . import db

class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    cpf = db.Column(db.String(11), unique = True)
    genre = db.Column(db.CHAR(1), nullable=True)
    date_of_birth = db.Column(db.Date, nullable=True)
    church_id = db.Column(db.Integer, db.ForeignKey('church.id'), nullable=False)
    type_person_id = db.Column(db.Integer, db.ForeignKey('type_person.id'), nullable=False)

    church = db.relationship('Church', backref='members')  # Relacionamento
    type_person = db.relationship('TypePerson', backref='members')  # Relacionamento

    def __repr__(self):
        return f"Membro ('{self.name}' )"
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'cpf': self.cpf,
            'church_id': self.church_id,
            'type_person_id': self.type_person_id,
            'date_of_birth': self.date_of_birth.isoformat() if self.date_of_birth else None 
        }