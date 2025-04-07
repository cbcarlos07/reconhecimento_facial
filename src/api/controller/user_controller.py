


from api.controller.base_controller import BaseController
from core.services.user_service import UserService

class UserController(BaseController):
    def __init__(self):
        self.user_service = UserService()
        super().__init__( self.user_service )

    
    