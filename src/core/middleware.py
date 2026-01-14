"""
Middleware de logging e métricas.
Registra todas as chamadas de API com logs estruturados e coleta métricas de performance.
"""
import time
import json
from datetime import datetime
from typing import Dict, List, Any
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from src.core.logging import logger


# Armazenamento em memória para métricas (em produção, usar Redis ou banco de dados)
class MetricsStore:
    """Armazena métricas de performance da API em memória."""
    
    def __init__(self, max_entries: int = 10000):
        self.max_entries = max_entries
        self.requests: List[Dict[str, Any]] = []
        self.stats = {
            "total_requests": 0,
            "total_errors": 0,
            "endpoints": {},
            "status_codes": {},
            "methods": {},
            "start_time": datetime.utcnow().isoformat()
        }
    
    def add_request(self, request_data: Dict[str, Any]):
        """Adiciona uma requisição ao histórico."""
        self.requests.append(request_data)
        
        # Mantém apenas as últimas N entradas
        if len(self.requests) > self.max_entries:
            self.requests = self.requests[-self.max_entries:]
        
        # Atualiza estatísticas
        self.stats["total_requests"] += 1
        
        endpoint = request_data.get("endpoint", "unknown")
        method = request_data.get("method", "unknown")
        status = str(request_data.get("status_code", 0))
        
        # Contagem por endpoint
        if endpoint not in self.stats["endpoints"]:
            self.stats["endpoints"][endpoint] = {"count": 0, "total_time": 0, "errors": 0}
        self.stats["endpoints"][endpoint]["count"] += 1
        self.stats["endpoints"][endpoint]["total_time"] += request_data.get("duration_ms", 0)
        
        # Contagem por status code
        if status not in self.stats["status_codes"]:
            self.stats["status_codes"][status] = 0
        self.stats["status_codes"][status] += 1
        
        # Contagem por método HTTP
        if method not in self.stats["methods"]:
            self.stats["methods"][method] = 0
        self.stats["methods"][method] += 1
        
        # Contagem de erros (4xx e 5xx)
        if request_data.get("status_code", 0) >= 400:
            self.stats["total_errors"] += 1
            self.stats["endpoints"][endpoint]["errors"] += 1
    
    def get_metrics(self) -> Dict[str, Any]:
        """Retorna métricas consolidadas."""
        # Calcula tempo médio por endpoint
        endpoint_stats = {}
        for endpoint, data in self.stats["endpoints"].items():
            avg_time = data["total_time"] / data["count"] if data["count"] > 0 else 0
            endpoint_stats[endpoint] = {
                "requests": data["count"],
                "avg_response_time_ms": round(avg_time, 2),
                "errors": data["errors"],
                "error_rate": round((data["errors"] / data["count"]) * 100, 2) if data["count"] > 0 else 0
            }
        
        return {
            "summary": {
                "total_requests": self.stats["total_requests"],
                "total_errors": self.stats["total_errors"],
                "error_rate": round((self.stats["total_errors"] / self.stats["total_requests"]) * 100, 2) if self.stats["total_requests"] > 0 else 0,
                "uptime_since": self.stats["start_time"]
            },
            "by_endpoint": endpoint_stats,
            "by_status_code": self.stats["status_codes"],
            "by_method": self.stats["methods"]
        }
    
    def get_recent_requests(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Retorna as requisições mais recentes."""
        return self.requests[-limit:][::-1]


# Instância global do store de métricas
metrics_store = MetricsStore()


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware para logging estruturado e coleta de métricas.
    Registra cada requisição com informações detalhadas.
    """
    
    async def dispatch(self, request: Request, call_next):
        """Processa a requisição e registra logs/métricas."""
        # Captura tempo inicial
        start_time = time.time()
        
        # Informações da requisição
        request_id = f"{int(start_time * 1000)}"
        client_ip = request.client.host if request.client else "unknown"
        method = request.method
        path = request.url.path
        query = str(request.query_params) if request.query_params else ""
        
        # Processa a requisição
        try:
            response = await call_next(request)
            status_code = response.status_code
            error = None
        except Exception as e:
            status_code = 500
            error = str(e)
            raise
        finally:
            # Calcula duração
            duration_ms = round((time.time() - start_time) * 1000, 2)
            
            # Monta log estruturado
            log_data = {
                "request_id": request_id,
                "timestamp": datetime.utcnow().isoformat(),
                "client_ip": client_ip,
                "method": method,
                "endpoint": path,
                "query_params": query,
                "status_code": status_code,
                "duration_ms": duration_ms,
                "error": error
            }
            
            # Registra métricas
            metrics_store.add_request(log_data)
            
            # Log estruturado em JSON
            log_level = "ERROR" if status_code >= 400 else "INFO"
            log_message = json.dumps(log_data, ensure_ascii=False)
            
            if status_code >= 500:
                logger.error(f"REQUEST: {log_message}")
            elif status_code >= 400:
                logger.warning(f"REQUEST: {log_message}")
            else:
                logger.info(f"REQUEST: {log_message}")
        
        return response
