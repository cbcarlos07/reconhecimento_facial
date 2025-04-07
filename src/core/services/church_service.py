
#src/core/services/church_service.py

from core.repositories.church_repository import ChurchRepository
from core.services.base_service import BaseService

class ChurchService(BaseService):
    def __init__(self):
        self.repository = ChurchRepository()
        super().__init__(self.repository)