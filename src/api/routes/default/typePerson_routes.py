#src/api/routes/default/service_routes.py
from api.controller.typePerson_controller import TypePersonController
from api.routes.base_router import BaseRouter

class TypePersonRoutes(BaseRouter):
    def __init__(self, app):
        self.controller = TypePersonController()
        super().__init__(app, self.controller)
        self.prefix = '/type-person'
    