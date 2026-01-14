"""
Endpoints de métricas e monitoramento.
Fornece acesso às métricas de performance da API.
"""
from fastapi import APIRouter
from typing import Dict, Any, List
from src.core.middleware import metrics_store

router = APIRouter()


@router.get(
    "/",
    response_model=Dict[str, Any],
    summary="Métricas consolidadas",
    description="Retorna métricas consolidadas de performance da API: total de requisições, erros, tempo médio por endpoint."
)
def get_metrics():
    """Retorna métricas de performance da API."""
    return metrics_store.get_metrics()


@router.get(
    "/requests",
    response_model=List[Dict[str, Any]],
    summary="Requisições recentes",
    description="Retorna as últimas requisições recebidas pela API com detalhes de tempo, status e endpoint."
)
def get_recent_requests(limit: int = 100):
    """Retorna as requisições mais recentes."""
    return metrics_store.get_recent_requests(limit)


@router.get(
    "/summary",
    response_model=Dict[str, Any],
    summary="Resumo rápido",
    description="Retorna um resumo rápido das métricas principais."
)
def get_summary():
    """Retorna resumo das métricas."""
    metrics = metrics_store.get_metrics()
    return {
        "status": "online",
        "total_requests": metrics["summary"]["total_requests"],
        "error_rate": f"{metrics['summary']['error_rate']}%",
        "uptime_since": metrics["summary"]["uptime_since"],
        "top_endpoints": sorted(
            metrics["by_endpoint"].items(),
            key=lambda x: x[1]["requests"],
            reverse=True
        )[:5]
    }
