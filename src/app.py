# src/app.py
from flask_migrate import Migrate
from server.server import Server
from config.database.models import db

# Inicializando a instância da aplicação
def initialize_app():
    server = Server()
    return server.get_app()  # Retorna a instância da aplicação Flask

# Inicializando a aplicação
app = initialize_app()

#db.init_app( app )
# Inicializando o Migrate
migrate = Migrate(app, db)

# Garantir que o banco de dados seja inicializado
with app.app_context():
    db.create_all()
    print("Banco de dados inicializado e tabelas criadas!")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)