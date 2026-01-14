"""
Dependências da API (Injeção de Dependências).
Fornece instâncias de repositórios e serviços para os endpoints.
"""
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from src.core.database import get_db
from src.repository.sqlalchemy_repository import SQLAlchemyBookRepository
from src.services.book_service import BookService
from src.services.stats_service import StatsService
from src.services.ml_service import MLService
from src.services.auth_service import verify_token, get_user_by_username
from src.models.user import UserModel

# Esquema OAuth2 para extração do token do header Authorization
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_book_repository(db: Session = Depends(get_db)) -> SQLAlchemyBookRepository:
    """Retorna uma instância do repositório de livros."""
    return SQLAlchemyBookRepository(db)

def get_book_service(repo: SQLAlchemyBookRepository = Depends(get_book_repository)) -> BookService:
    """Retorna uma instância do serviço de livros."""
    return BookService(repo)

def get_stats_service(repo: SQLAlchemyBookRepository = Depends(get_book_repository)) -> StatsService:
    """Retorna uma instância do serviço de estatísticas."""
    return StatsService(repo)

def get_ml_service(repo: SQLAlchemyBookRepository = Depends(get_book_repository)) -> MLService:
    """Retorna uma instância do serviço de ML."""
    return MLService(repo)

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> UserModel:
    """
    Extrai e valida o usuário a partir do token JWT.
    Usado como dependência em rotas protegidas.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido ou expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = verify_token(token, token_type="access")
    if not payload:
        raise credentials_exception
    
    username: str = payload.get("sub")
    if not username:
        raise credentials_exception
    
    user = get_user_by_username(db, username)
    if not user or not user.is_active:
        raise credentials_exception
    
    return user

def get_current_admin_user(
    current_user: UserModel = Depends(get_current_user)
) -> UserModel:
    """
    Verifica se o usuário atual é um administrador.
    Usado como dependência em rotas que requerem privilégios de admin.
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado. Privilégios de administrador requeridos."
        )
    return current_user

