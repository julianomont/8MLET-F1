"""
Endpoints relacionados a livros.
Fornece operações de listagem, busca e filtros.
"""
from fastapi import APIRouter, Depends, Query, Path
from typing import List, Optional
from src.api.deps import get_book_service
from src.services.book_service import BookService
from src.schemas.responses import BookResponse, PaginatedBooks
from src.core.exceptions import handle_not_found_exception

router = APIRouter()

@router.get(
    "/",
    response_model=PaginatedBooks,
    summary="Listar livros",
    description="Retorna uma lista paginada de todos os livros disponíveis."
)
def list_books(
    page: int = Query(1, ge=1, description="Número da página"),
    limit: int = Query(50, ge=1, le=100, description="Quantidade de itens por página"),
    service: BookService = Depends(get_book_service)
):
    """Lista todos os livros com paginação."""
    books, total = service.get_books_paginated(page, limit)
    return PaginatedBooks(
        total=total,
        page=page,
        limit=limit,
        items=[book.dict() for book in books]
    )

@router.get(
    "/search",
    response_model=List[BookResponse],
    summary="Buscar livros",
    description="Busca livros por título e/ou categoria."
)
def search_books(
    title: Optional[str] = Query(None, description="Título do livro (busca parcial)"),
    category: Optional[str] = Query(None, description="Categoria do livro"),
    service: BookService = Depends(get_book_service)
):
    """Busca livros por título ou categoria."""
    books = service.search_books(title, category)
    return [book.dict() for book in books]

@router.get(
    "/top-rated",
    response_model=List[BookResponse],
    summary="Livros mais bem avaliados",
    description="Retorna os livros com as melhores avaliações."
)
def get_top_rated(
    limit: int = Query(10, ge=1, le=50, description="Quantidade de livros a retornar"),
    service: BookService = Depends(get_book_service)
):
    """Retorna os livros mais bem avaliados."""
    books = service.get_top_rated(limit)
    return [book.dict() for book in books]

@router.get(
    "/price-range",
    response_model=List[BookResponse],
    summary="Filtrar por faixa de preço",
    description="Retorna livros dentro de uma faixa de preço específica."
)
def get_by_price_range(
    min_price: float = Query(0.0, description="Preço mínimo"),
    max_price: float = Query(1000.0, description="Preço máximo"),
    service: BookService = Depends(get_book_service)
):
    """Filtra livros por faixa de preço."""
    if min_price > max_price:
        return []
    books = service.get_by_price_range(min_price, max_price)
    return [book.dict() for book in books]

@router.get(
    "/{book_id}",
    response_model=BookResponse,
    summary="Detalhes do livro",
    description="Retorna os detalhes de um livro específico pelo seu ID."
)
def get_book(
    book_id: int = Path(..., ge=1, description="ID único do livro"),
    service: BookService = Depends(get_book_service)
):
    """Busca um livro pelo ID."""
    book = service.get_book_by_id(book_id)
    if not book:
        handle_not_found_exception(f"Livro com id {book_id} não encontrado")
    return book.dict()
