
#src/core/services/service_service.py
from datetime import time
from core.repositories.service_repository import ServiceRepository
from core.services.base_service import BaseService

class ServiceService(BaseService):
    def __init__(self):
        self.repository = ServiceRepository()
        super().__init__(self.repository)

    def create(self, data):
        # Converte strings de hora para objetos time do Python
        if 'hour_start' in data and isinstance(data['hour_start'], str):
            hours, minutes, seconds = map(int, data['hour_start'].split(':'))
            data['hour_start'] = time(hours, minutes, seconds)
        
        if 'hour_end' in data and isinstance(data['hour_end'], str):
            hours, minutes, seconds = map(int, data['hour_end'].split(':'))
            data['hour_end'] = time(hours, minutes, seconds)
            
        return super().create(data)