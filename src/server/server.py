from flask import Flask
from flask_cors import CORS

from api.routes import register_all_routes
from config.database.config import Config

from config.database.models import  init_db, setup_db_session, db
class Server:
    def __init__(self):
        self.app = Flask(__name__)
        CORS(self.app)
        self.app.config['JSON_SORT_KEYS'] = False
        self.app.config.from_object( Config )
        self.db = init_db(self.app)
        
        # Configura a sessão do banco de dados
        self.db_session = setup_db_session(self.app)
        self.routes()
        

    def run(self, host, port):
        self.app.run(host=host, port=port, debug=True)
    
    def routes(self):
        # Registra todas as rotas automaticamente
        register_all_routes(self.app)


    def get_app(self):
        return self.app
    
    def get_db_session(self):
        return self.db_session
        