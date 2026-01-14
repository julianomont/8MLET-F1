"""
Endpoints de estatísticas.
Fornece métricas e análises sobre os livros.
"""
from fastapi import APIRouter, Depends
from typing import Dict, Any, List
from src.api.deps import get_stats_service
from src.services.stats_service import StatsService
from src.schemas.responses import CategoryStats

router = APIRouter()

@router.get(
    "/overview",
    response_model=Dict[str, Any],
    summary="Visão geral",
    description="Retorna estatísticas gerais sobre todos os livros: total, preço médio, distribuição de avaliações e categorias mais populares."
)
def get_stats_overview(
    service: StatsService = Depends(get_stats_service)
):
    """Retorna visão geral das estatísticas."""
    return service.get_overview()

@router.get(
    "/categories",
    response_model=List[CategoryStats],
    summary="Estatísticas por categoria",
    description="Retorna estatísticas detalhadas para cada categoria: quantidade de livros, preço médio e avaliação média."
)
def get_category_stats(
    service: StatsService = Depends(get_stats_service)
):
    """Retorna estatísticas por categoria."""
    return service.get_category_stats()
