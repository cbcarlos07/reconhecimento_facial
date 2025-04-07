#src/core/repositories/repository.py
from config.database.models import db
class Repository:
    def __init__(self, model):
        self.model = model
        self.db = db

    def get_all(self):
        models = self.model.query.all()  # Obtém todos os usuários
        return [model.to_dict() for model in models]
    
    def get_by_id(self, id):
        data = self.model.query.get(id)  # Obtém o usuário pelo ID
        return data.to_dict()
    
    def create(self, data):
        new_data = self.model(**data)
        
        # Adiciona à sessão do SQLAlchemy
        self.db.session.add(new_data)
        
        # Confirma a transação
        self.db.session.commit()
        
        return new_data.to_dict()
    
    def update(self, id, data):
        model = self.model.query.get(id)  # Obtém o usuário pelo ID
        if model:
            for key, value in data.items():  # Atualiza os campos
                setattr(model, key, value)
            self.db.session.commit()  # Salva as alterações
            return model.to_dict()  # Retorna usuário atualizado
        

    
    def delete(self, id):
        model = self.model.query.get(id)  # Obtém o usuário pelo ID
        if model:
            self.db.session.delete(model)  # Remove o usuário
            self.db.session.commit()  # Salva as alterações
            return True
        else: 
            return False
          