from core.repositories.repository import Repository
from config.database.models import User

class UserRepository(Repository):
    def __init__(self):
        super().__init__(User)
        
    
    