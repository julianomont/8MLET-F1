"""
Serviço de Machine Learning.
Prepara features dos livros para treinamento de modelos.
"""
import pandas as pd
from typing import List, Dict, Any, Optional
from src.repository.base import BaseRepository
from src.schemas.responses import BookBase as Book

class MLService:
    """Serviço para preparação de features para ML."""
    
    def __init__(self, repository: BaseRepository[Book]):
        """Inicializa o serviço com um repositório."""
        self.repository = repository

    def get_features(self) -> List[Dict[str, Any]]:
        """Retorna features prontas para treinamento de modelos."""
        books = self.repository.get_all()
        if not books:
            return []
        
        # Converte para DataFrame
        df = pd.DataFrame([b.dict() for b in books])
        
        # Codifica categorias como números
        df['category_code'] = df['category'].astype('category').cat.codes
        
        # Normaliza preços (Min-Max)
        if len(df) > 0:
            df['price_norm'] = (df['price'] - df['price'].min()) / (df['price'].max() - df['price'].min())
        else:
            df['price_norm'] = 0
        
        # Retorna features selecionadas
        features = df[['id', 'price_norm', 'rating', 'category_code', 'availability']].to_dict('records')
        return features

    def get_training_data(self, test_size: float = 0.2) -> Dict[str, Any]:
        """
        Retorna dataset completo para treinamento de modelos ML.
        Inclui features, labels e metadados do dataset.
        
        Args:
            test_size: Proporção de dados para teste (0.0 a 1.0)
        
        Returns:
            Dicionário com train/test splits e metadados
        """
        books = self.repository.get_all()
        if not books:
            return {"error": "Nenhum dado disponível", "total_samples": 0}
        
        # Converte para DataFrame
        df = pd.DataFrame([b.dict() for b in books])
        
        # Codifica categorias
        category_mapping = {cat: idx for idx, cat in enumerate(df['category'].unique())}
        df['category_code'] = df['category'].map(category_mapping)
        
        # Normaliza preços (Min-Max)
        price_min = df['price'].min()
        price_max = df['price'].max()
        df['price_norm'] = (df['price'] - price_min) / (price_max - price_min)
        
        # Converte disponibilidade para int
        df['availability_int'] = df['availability'].astype(int)
        
        # Features para treinamento
        feature_columns = ['price_norm', 'rating', 'category_code', 'availability_int']
        X = df[feature_columns].values.tolist()
        
        # Label: rating como target (para predição de avaliação)
        y = df['rating'].values.tolist()
        
        # Split treino/teste
        split_idx = int(len(X) * (1 - test_size))
        
        return {
            "total_samples": len(X),
            "feature_names": feature_columns,
            "target_name": "rating",
            "train": {
                "X": X[:split_idx],
                "y": y[:split_idx],
                "size": split_idx
            },
            "test": {
                "X": X[split_idx:],
                "y": y[split_idx:],
                "size": len(X) - split_idx
            },
            "metadata": {
                "category_mapping": category_mapping,
                "price_min": price_min,
                "price_max": price_max,
                "test_size": test_size
            }
        }

    def save_prediction(self, predictions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Processa e armazena predições recebidas de modelos ML.
        
        Args:
            predictions: Lista de predições com book_id e predicted_rating
        
        Returns:
            Resumo das predições processadas
        """
        if not predictions:
            return {"error": "Nenhuma predição recebida", "processed": 0}
        
        # Valida e processa predições
        valid_predictions = []
        invalid_predictions = []
        
        for pred in predictions:
            book_id = pred.get("book_id")
            predicted_rating = pred.get("predicted_rating")
            
            # Valida campos obrigatórios
            if book_id is None or predicted_rating is None:
                invalid_predictions.append({"prediction": pred, "error": "Campos obrigatórios faltando"})
                continue
            
            # Valida range do rating
            if not (1 <= predicted_rating <= 5):
                invalid_predictions.append({"prediction": pred, "error": "Rating deve estar entre 1 e 5"})
                continue
            
            valid_predictions.append({
                "book_id": book_id,
                "predicted_rating": round(predicted_rating, 2),
                "confidence": pred.get("confidence", None)
            })
        
        return {
            "processed": len(valid_predictions),
            "rejected": len(invalid_predictions),
            "predictions": valid_predictions,
            "errors": invalid_predictions if invalid_predictions else None
        }

