"""
Endpoints relacionados a categorias de livros.
"""
from fastapi import APIRouter, Depends
from typing import List
from src.api.deps import get_book_service
from src.services.book_service import BookService

router = APIRouter()

@router.get(
    "/",
    response_model=List[str],
    summary="Listar categorias",
    description="Retorna todas as categorias de livros disponíveis."
)
def list_categories(
    service: BookService = Depends(get_book_service)
):
    """Lista todas as categorias disponíveis."""
    return service.get_all_categories()
