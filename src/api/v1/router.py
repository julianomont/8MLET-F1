"""
Roteador principal da API v1.
Agrupa todos os endpoints em um único roteador.
"""
from fastapi import APIRouter
from src.api.v1.endpoints import books, categories, health, stats, ml, auth, scraping, metrics

# Roteador principal da API
api_router = APIRouter()

# Inclui os sub-roteadores com seus prefixos e tags
api_router.include_router(health.router, prefix="/health", tags=["Saúde"])
api_router.include_router(auth.router, prefix="/auth", tags=["Autenticação"])
api_router.include_router(books.router, prefix="/books", tags=["Livros"])
api_router.include_router(categories.router, prefix="/categories", tags=["Categorias"])
api_router.include_router(stats.router, prefix="/stats", tags=["Estatísticas"])
api_router.include_router(ml.router, prefix="/ml", tags=["Machine Learning"])
api_router.include_router(scraping.router, prefix="/scraping", tags=[])
api_router.include_router(metrics.router, prefix="/metrics", tags=["Métricas"])
