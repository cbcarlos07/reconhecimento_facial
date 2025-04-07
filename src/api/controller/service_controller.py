


from api.controller.base_controller import BaseController
from core.services.service_service import ServiceService

class ServiceController(BaseController):
    def __init__(self):
        self.service = ServiceService()
        super().__init__( self.service )

    
    