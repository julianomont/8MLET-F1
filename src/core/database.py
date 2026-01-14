"""
Configuração do banco de dados SQLite.
Utiliza SQLAlchemy como ORM.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from src.core.config import settings

# Cria o engine de conexão com o banco
engine = create_engine(
    settings.DATABASE_URL, connect_args={"check_same_thread": False}
)

# Fábrica de sessões
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Classe base para os models
Base = declarative_base()

def get_db():
    """Retorna uma sessão do banco de dados."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
