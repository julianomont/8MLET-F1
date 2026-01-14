"""
Model SQLAlchemy para livros.
Define a estrutura da tabela no banco de dados.
"""
from sqlalchemy import Column, Integer, String, Float, Boolean
from src.core.database import Base

class BookModel(Base):
    """Modelo de livro no banco de dados."""
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)          # ID único
    title = Column(String, index=True)                          # Título do livro
    price = Column(Float)                                       # Preço em libras
    rating = Column(Integer)                                    # Avaliação (1-5)
    availability = Column(Boolean)                              # Disponível em estoque
    category = Column(String, index=True)                       # Categoria do livro
    image_url = Column(String)                                  # URL da imagem de capa
