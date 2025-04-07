# core/database/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

# Configure a conexão com o banco de dados
DATABASE_URL = "sqlite:///site.db"  # Ajuste conforme necessário
engine = create_engine(DATABASE_URL)

# Crie uma sessão do banco de dados
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

# Base para os modelos declarativos
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    """Inicializa o banco de dados criando todas as tabelas definidas."""
    Base.metadata.create_all(bind=engine)