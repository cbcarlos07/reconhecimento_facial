#src/config/database/models/__init__.py
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine


# Instância do SQLAlchemy
db = SQLAlchemy()
# Esta função será chamada para inicializar o banco de dados
def init_db(app):
    db.init_app(app)
    
    # Cria todas as tabelas
    with app.app_context():
        db.create_all()
    
    return db

# Configuração da sessão do SQLAlchemy
def setup_db_session(app):
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db_session = scoped_session(Session)
    return db_session


# Importando os modelos
from .user import User
from .service import Service
from .type_person import TypePerson
from .member import Member
from .church import Church
