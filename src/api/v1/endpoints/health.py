"""
Endpoint de verificação de saúde da API.
Verifica status da API e conectividade com os dados.
"""
from fastapi import APIRouter, Depends
from datetime import datetime
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.models.book import BookModel

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
        db_status = "conectado"
    except Exception as e:
        books_count = 0
        db_status = f"erro: {str(e)}"
    
    return {
        "status": "saudável" if db_status == "conectado" else "degradado",
        "version": "1.0.0",
        "database": db_status,
        "books_count": books_count,
        "timestamp": datetime.now().isoformat()
    }

