"""
Exceções personalizadas da API.
Define erros específicos do sistema.
"""
from fastapi import HTTPException, status

class BooksAPIException(Exception):
    """Exceção base para a Books API."""
    pass

class ScraperError(BooksAPIException):
    """Erro durante o processo de scraping."""
    pass

class DataNotFoundError(BooksAPIException):
    """Dados não encontrados no repositório."""
    pass

def handle_not_found_exception(detail: str = "Recurso não encontrado"):
    """Lança exceção HTTP 404 para recurso não encontrado."""
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=detail
    )
