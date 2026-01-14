"""
Exportador de dados.
Salva os livros extraídos no banco de dados.
"""
from typing import List
from src.schemas.responses import BookBase as Book
from src.core.database import SessionLocal, engine, Base
from src.models.book import BookModel
from src.repository.sqlalchemy_repository import SQLAlchemyBookRepository
from src.core.logging import logger

class DataExporter:
    """Classe para exportar dados para o banco."""
    
    @staticmethod
    def export_to_db(books: List[Book]):
        """Exporta lista de livros para o SQLite."""
        logger.info(f"Exportando {len(books)} livros para SQLite...")
        
        # Garante que as tabelas existem
        Base.metadata.create_all(bind=engine)
        
        # Salva no banco
        db = SessionLocal()
        try:
            repo = SQLAlchemyBookRepository(db)
            repo.save_all(books)
            logger.info("Exportação para SQLite concluída.")
        finally:
            db.close()
