"""
Serviço de livros.
Contém a lógica de negócio para operações com livros.
"""
from typing import List, Optional, Tuple
from src.repository.base import BaseRepository
from src.schemas.responses import BookBase as Book

class BookService:
    """Serviço para operações com livros."""
    
    def __init__(self, repository: BaseRepository[Book]):
        """Inicializa o serviço com um repositório."""
        self.repository = repository

    def get_books_paginated(self, page: int, limit: int) -> Tuple[List[Book], int]:
        """Retorna livros paginados e o total de livros."""
        all_books = self.repository.get_all()
        start = (page - 1) * limit
        end = start + limit
        return all_books[start:end], len(all_books)

    def get_book_by_id(self, id: int) -> Optional[Book]:
        """Busca um livro pelo ID."""
        return self.repository.get_by_id(id)

    def search_books(self, title: Optional[str] = None, category: Optional[str] = None) -> List[Book]:
        """Busca livros por título e/ou categoria."""
        return self.repository.find(title=title, category=category)

    def get_top_rated(self, limit: int = 10) -> List[Book]:
        """Retorna os livros mais bem avaliados."""
        all_books = self.repository.get_all()
        # Ordena por avaliação decrescente, depois preço crescente
        sorted_books = sorted(all_books, key=lambda x: (-x.rating, x.price))
        return sorted_books[:limit]

    def get_by_price_range(self, min_price: float, max_price: float) -> List[Book]:
        """Retorna livros dentro de uma faixa de preço."""
        all_books = self.repository.get_all()
        return [b for b in all_books if min_price <= b.price <= max_price]
        
    def get_all_categories(self) -> List[str]:
        """Retorna todas as categorias disponíveis."""
        return self.repository.get_categories()
