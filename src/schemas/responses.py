"""
Schemas de resposta da API.
Define os modelos de dados para respostas.
"""
from pydantic import BaseModel, validator
from typing import List, Optional

class BookBase(BaseModel):
    """Schema base para livros."""
    id: Optional[int] = None       # ID do livro
    title: str                     # Título
    price: float                   # Preço
    rating: int                    # Avaliação (1-5)
    availability: bool             # Disponibilidade
    category: str                  # Categoria
    image_url: str                 # URL da imagem
    
    @validator("rating")
    def validate_rating(cls, v):
        """Valida que a avaliação está entre 1 e 5."""
        if not (1 <= v <= 5):
            raise ValueError("Avaliação deve ser entre 1 e 5")
        return v

class BookResponse(BookBase):
    """Schema de resposta para livro com ID obrigatório."""
    id: int

class PaginatedBooks(BaseModel):
    """Schema para resposta paginada de livros."""
    total: int                     # Total de livros
    page: int                      # Página atual
    limit: int                     # Itens por página
    items: List[BookResponse]      # Lista de livros

class CategoryStats(BaseModel):
    """Schema para estatísticas de categoria."""
    category: str                  # Nome da categoria
    count: int                     # Quantidade de livros
    avg_price: float               # Preço médio
    avg_rating: float              # Avaliação média

class HealthResponse(BaseModel):
    """Schema para resposta de health check."""
    status: str                    # Status da API
    version: str                   # Versão
    timestamp: str                 # Data/hora da verificação
