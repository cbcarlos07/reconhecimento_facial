#src/core/repositories/church.py
from core.repositories.repository import Repository
from config.database.models import Church

class ChurchRepository(Repository):
    def __init__(self):
        super().__init__(Church)
        
    
    