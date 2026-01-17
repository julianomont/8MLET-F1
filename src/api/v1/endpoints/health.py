"""
Endpoint de verificação de saúde da API.
Verifica status da API e conectividade com os dados.
"""
from fastapi import APIRouter, Depends
from datetime import datetime
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.models.book import BookModel
from src.models.user import UserModel

router = APIRouter()


@router.get(
    "",
    summary="Verificação de saúde",
    description="Verifica se a API está funcionando corretamente e a conectividade com os dados."
)
def health_check(db: Session = Depends(get_db)):
    """
    Verifica o status de saúde da API.
    
    Retorna:
    - status: estado geral da API
    - version: versão da API
    - database: status de conexão com banco de dados
    - books_count: quantidade de livros no banco
    - timestamp: data/hora da verificação
    """
    # Verifica conectividade com o banco
    try:
        books_count = db.query(BookModel).count()
        users_count = db.query(UserModel).count()
        admin_exists = db.query(UserModel).filter(UserModel.username == "admin").first() is not None
        db_status = "conectado"
    except Exception as e:
        books_count = 0
        users_count = 0
        admin_exists = False
        db_status = f"erro: {str(e)}"
    
    return {
        "status": "saudável" if db_status == "conectado" else "degradado",
        "version": "1.0.0",
        "database": db_status,
        "books_count": books_count,
        "users_count": users_count,
        "admin_exists": admin_exists,
        "timestamp": datetime.now().isoformat()
    }

