"""
Repositório SQLAlchemy para livros.
Implementa operações de banco de dados usando SQLAlchemy.
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from src.repository.base import BaseRepository
from src.schemas.responses import BookBase as BookSchema
from src.models.book import BookModel

class SQLAlchemyBookRepository(BaseRepository[BookSchema]):
    """Repositório de livros usando SQLAlchemy."""
    
    def __init__(self, db: Session):
        """Inicializa com uma sessão do banco."""
        self.db = db

    def get_all(self) -> List[BookSchema]:
        """Retorna todos os livros."""
        db_books = self.db.query(BookModel).all()
        return [self._to_schema(b) for b in db_books]

    def get_by_id(self, id: int) -> Optional[BookSchema]:
        """Busca um livro pelo ID."""
        db_book = self.db.query(BookModel).filter(BookModel.id == id).first()
        return self._to_schema(db_book) if db_book else None

    def find(self, title: Optional[str] = None, category: Optional[str] = None) -> List[BookSchema]:
        """Busca livros por título e/ou categoria."""
        query = self.db.query(BookModel)
        if title:
            query = query.filter(BookModel.title.ilike(f"%{title}%"))
        if category:
            query = query.filter(BookModel.category == category)
        return [self._to_schema(b) for b in query.all()]

    def get_categories(self) -> List[str]:
        """Retorna todas as categorias distintas."""
        categories = self.db.query(BookModel.category).distinct().all()
        return sorted([c[0] for c in categories])

    def save_all(self, books: List[BookSchema]):
        """Salva uma lista de livros no banco."""
        # Limpa registros existentes
        self.db.query(BookModel).delete()
        
        # Insere novos registros
        for book in books:
            db_book = BookModel(
                title=book.title,
                price=book.price,
                rating=book.rating,
                availability=book.availability,
                category=book.category,
                image_url=book.image_url
            )
            self.db.add(db_book)
        self.db.commit()

    def _to_schema(self, db_book: BookModel) -> BookSchema:
        """Converte model para schema."""
        return BookSchema(
            id=db_book.id,
            title=db_book.title,
            price=db_book.price,
            rating=db_book.rating,
            availability=db_book.availability,
            category=db_book.category,
            image_url=db_book.image_url
        )
