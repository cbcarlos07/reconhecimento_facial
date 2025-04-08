


from api.controller.base_controller import BaseController
from core.services.typePerson_service import TypePersonService

class TypePersonController(BaseController):
    def __init__(self):
        self.service = TypePersonService()
        super().__init__( self.service )

    
    