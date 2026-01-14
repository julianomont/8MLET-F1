"""
Endpoints para Machine Learning.
Fornece features e dados preparados para treinamento de modelos.
"""
from fastapi import APIRouter, Depends, Query
from typing import List, Dict, Any
from pydantic import BaseModel
from src.api.deps import get_ml_service
from src.services.ml_service import MLService


class PredictionInput(BaseModel):
    """Schema para entrada de predições."""
    book_id: int
    predicted_rating: float
    confidence: float = None


class PredictionsRequest(BaseModel):
    """Schema para requisição de predições."""
    predictions: List[PredictionInput]


router = APIRouter()


@router.get(
    "/features",
    response_model=List[Dict[str, Any]],
    summary="Features para ML",
    description="Retorna dados dos livros formatados como features para inferência de modelos. Inclui preço normalizado, código da categoria e avaliação."
)
def get_ml_features(
    service: MLService = Depends(get_ml_service)
):
    """Retorna features prontas para inferência."""
    return service.get_features()


@router.get(
    "/training-data",
    response_model=Dict[str, Any],
    summary="Dataset para treinamento",
    description="Retorna dataset completo para treinamento de modelos ML, incluindo split treino/teste, features normalizadas e metadados."
)
def get_training_data(
    test_size: float = Query(0.2, ge=0.1, le=0.5, description="Proporção de dados para teste (0.1 a 0.5)"),
    service: MLService = Depends(get_ml_service)
):
    """Retorna dataset formatado para treinamento de modelos."""
    return service.get_training_data(test_size)


@router.post(
    "/predictions",
    response_model=Dict[str, Any],
    summary="Receber predições",
    description="Endpoint para receber e processar predições de modelos ML. Valida e armazena as predições recebidas."
)
def receive_predictions(
    request: PredictionsRequest,
    service: MLService = Depends(get_ml_service)
):
    """Recebe e processa predições de modelos externos."""
    predictions = [pred.dict() for pred in request.predictions]
    return service.save_prediction(predictions)

