#src/api/routes/base_router.py

import uuid
from flask import Blueprint


class BaseRouter:
    def __init__(self, app, controller):
        if controller is not None:
            self.controller = controller
            
        self.app = app
        self.prefix = "/"
        # Criar um nome único para o blueprint baseado no prefixo e em um ID aleatório
        prefix_name = self.prefix.strip('/').replace('/', '_') or 'root'
        unique_id = str(uuid.uuid4())[:8]  # Usar parte de um UUID para garantir unicidade
        self.blueprint = Blueprint(f"{prefix_name}_{unique_id}", __name__)

    def configure_routes(self):
        self.blueprint.route('/', methods=['GET'])(self.controller.get_all)
        self.blueprint.route('/<int:id>', methods=['GET'])(self.controller.get_by_id)
        self.blueprint.route('/', methods=['POST'])(self.controller.create)
        self.blueprint.route('/<int:id>', methods=['PUT'])(self.controller.update)
        self.blueprint.route('/<int:id>', methods=['DELETE'])(self.controller.delete)

        # Registrar o blueprint com o prefixo
        print(f"prefix {self.prefix}")
        self.app.register_blueprint(self.blueprint, url_prefix=self.prefix)