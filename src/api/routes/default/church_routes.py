#src/api/routes/default/service_routes.py
from api.controller.church_controller import ChurchController
from api.routes.base_router import BaseRouter

class ChurchRoutes(BaseRouter):
    def __init__(self, app):
        self.controller = ChurchController()
        super().__init__(app, self.controller)
        self.prefix = '/church'
    