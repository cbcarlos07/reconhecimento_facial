#src/api/routes/default/service_routes.py
from api.controller.member_controller import MemberController
from api.routes.base_router import BaseRouter

class MemberRoutes(BaseRouter):
    def __init__(self, app):
        self.controller = MemberController()
        super().__init__(app, self.controller)
        self.prefix = '/member'

    def configure_routes(self):
        self.blueprint.route('/church/<int:church_id>', methods=['GET'])(self.controller.get_all_by_church)
        super().configure_routes()
        
    