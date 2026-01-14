"""
Model SQLAlchemy para usuários.
Define a estrutura da tabela de usuários no banco de dados.
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from src.core.database import Base


class UserModel(Base):
    """Modelo de usuário no banco de dados."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)           # ID único
    username = Column(String, unique=True, index=True)           # Nome de usuário
    email = Column(String, unique=True, index=True)              # E-mail
    hashed_password = Column(String)                             # Senha hasheada
    is_active = Column(Boolean, default=True)                    # Usuário ativo
    is_admin = Column(Boolean, default=False)                    # É administrador
    created_at = Column(DateTime, default=datetime.utcnow)       # Data de criação
