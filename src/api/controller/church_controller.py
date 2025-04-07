


from api.controller.base_controller import BaseController
from core.services.church_service import ChurchService

class ChurchController(BaseController):
    def __init__(self):
        self.service = ChurchService()
        super().__init__( self.service )

    
    