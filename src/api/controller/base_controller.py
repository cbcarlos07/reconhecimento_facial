from flask import request, jsonify
class BaseController:
    def __init__(self, service):
        self.service = service
    
    def get_all(self):
        info = self.service.get_all()
        return jsonify(info), 200
    
    def get_by_id(self, id):
        try:
            info = self.service.get_by_id(id)
            if info:
                return jsonify(info), 200
            return jsonify({"error": "info not found"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    def create(self):
        try:
            data = request.get_json()
            info = self.service.create(data)
            return jsonify(info), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 400
    
    def update(self, id):
        try:
            data = request.get_json()
            info = self.service.update(id, data)
            if info:
                return jsonify(info), 200
            return jsonify({"error": "info not found"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 400
    
    def delete(self, id):
        try:
            success = self.service.delete(id)
            if success:
                return jsonify({"message": "data deleted successfully"}), 200
            return jsonify({"error": "data not found"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500