"""
Serviço de estatísticas.
Fornece análises e métricas sobre os livros.
"""
import pandas as pd
from typing import Dict, Any, List
from src.repository.base import BaseRepository
from src.schemas.responses import BookBase as Book
from src.schemas.responses import CategoryStats

class StatsService:
    """Serviço para estatísticas de livros."""
    
    def __init__(self, repository: BaseRepository[Book]):
        """Inicializa o serviço com um repositório."""
        self.repository = repository

    def get_overview(self) -> Dict[str, Any]:
        """Retorna estatísticas gerais dos livros."""
        books = self.repository.get_all()
        if not books:
            return {}
        
        # Converte para DataFrame para cálculos
        df = pd.DataFrame([b.dict() for b in books])
        
        return {
            "total_books": len(books),
            "avg_price": float(df['price'].mean()),
            "min_price": float(df['price'].min()),
            "max_price": float(df['price'].max()),
            "rating_distribution": df['rating'].value_counts().to_dict(),
            "top_categories": df['category'].value_counts().head(5).to_dict()
        }

    def get_category_stats(self) -> List[CategoryStats]:
        """Retorna estatísticas por categoria."""
        books = self.repository.get_all()
        if not books:
            return []
        
        # Agrupa por categoria e calcula estatísticas
        df = pd.DataFrame([b.dict() for b in books])
        stats = df.groupby('category').agg({
            'id': 'count',
            'price': 'mean',
            'rating': 'mean'
        }).reset_index()
        
        return [
            CategoryStats(
                category=row['category'],
                count=int(row['id']),
                avg_price=float(row['price']),
                avg_rating=float(row['rating'])
            ) for _, row in stats.iterrows()
        ]
