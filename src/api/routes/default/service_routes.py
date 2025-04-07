#src/api/routes/default/service_routes.py
from api.controller.service_controller import ServiceController
from api.routes.base_router import BaseRouter

class ServiceRoutes(BaseRouter):
    def __init__(self, app):
        self.controller = ServiceController()
        super().__init__(app, self.controller)
        self.prefix = '/service'
    