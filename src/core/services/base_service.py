#src/core/services/base_service.py
class BaseService:
    def __init__(self, repository):
        self.repository = repository

    def get_all(self):
        return self.repository.get_all()
    
    def get_by_id(self, id):
        return self.repository.get_by_id(id)
    
    def create(self, data):
        return self.repository.create(data)
    
    def update(self, id, data):
        # Validações de negócio
        if not data:
            raise ValueError("No data provided for update")
        
        return self.repository.update(id, data)
    
    def delete(self, id):
        return self.repository.delete(id)