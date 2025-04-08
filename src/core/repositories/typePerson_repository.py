#src/core/repositories/typePerson.py
from core.repositories.repository import Repository
from config.database.models import TypePerson

class TypePersonRepository(Repository):
    def __init__(self):
        super().__init__(TypePerson)    
    
    