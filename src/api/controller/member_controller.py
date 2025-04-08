#src/api/controller/member_controller.py
from api.controller.base_controller import BaseController
from core.services.member_service import MemberService

class MemberController(BaseController):
    def __init__(self):
        self.service = MemberService()
        super().__init__( self.service )

    def get_all_by_church(self, church_id):
        try:
            info = self.service.get_all_by_church(church_id)
            if info:
                return self.jsonify(info), 200
            return self.jsonify({"error": "info not found"}), 404
        except Exception as e:
            return self.jsonify({"error": str(e)}), 500
        