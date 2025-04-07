#src/config/database/models/service.py
from . import db

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    day = db.Column(db.Integer, nullable=False)
    hour_start = db.Column(db.Time, nullable=False)
    hour_end = db.Column(db.Time, nullable=False)
    enabled = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f"Service('{self.name}', {self.day}', '{self.hour_start}', '{self.hour_end}', '{self.enabled}')"
    
    def to_dict(self):
        """Converte o objeto User em um dicionário."""
        return {
            'id': self.id,
            'name': self.name,
            'day': self.day,
            'hour_start': self.hour_start.strftime('%H:%M:%S') if self.hour_start else None,
            'hour_end': self.hour_end.strftime('%H:%M:%S') if self.hour_end else None,
            'enabled': self.enabled
            # Note que não incluímos 'password' por segurança
        }