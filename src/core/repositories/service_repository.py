#src/core/repositories/service.py
from core.repositories.repository import Repository
from config.database.models import Service

class ServiceRepository(Repository):
    def __init__(self):
        super().__init__(Service)
        
    
    