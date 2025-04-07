#src/api/routes/default/user_routes.py
from api.controller.user_controller import UserController
from api.routes.base_router import BaseRouter

class UserRoutes(BaseRouter):
    def __init__(self, app):
        self.controller = UserController()
        super().__init__(app, self.controller)
        self.prefix = '/users'
    