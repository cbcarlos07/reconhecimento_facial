from flask import jsonify

class InitRoutes:
    def __init__(self, app):
        self.app = app
        self.prefix = '/'

    def configure_routes(self):
        self.app.route(self.prefix, methods=['GET'])(
            lambda: jsonify({'msg': 'Bem-vindo à API de marcação de presença da Igreja'})
        )
