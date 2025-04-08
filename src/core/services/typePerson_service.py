
#src/core/services/typePerson.py

from core.repositories.typePerson_repository import TypePersonRepository
from core.services.base_service import BaseService

class TypePersonService(BaseService):
    def __init__(self):
        self.repository = TypePersonRepository()
        super().__init__(self.repository)