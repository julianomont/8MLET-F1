"""
Configurações da aplicação.
Carrega variáveis de ambiente e define valores padrão.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
from typing import Optional, Any

class Settings(BaseSettings):
    """Configurações gerais da API."""
    
    # Informações do projeto
    PROJECT_NAME: str = "API de Livros"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = True
    
    # Configurações de scraping
    SCRAPE_URL: str = "http://books.toscrape.com"
    MAX_RETRIES: int = 3
    RETRY_DELAY: int = 5
    
    # Caminhos do sistema
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    DATA_PATH: Path = BASE_DIR / "data" / "processed" / "books.csv"
    
    
    # Define o caminho do banco de dados (Obrigatório via environment)
    DATABASE_URL: Optional[str] = None

    def model_post_init(self, __context: Any):
        if not self.DATABASE_URL:
             # Tenta ler do ambiente explicitamente se não veio pelo pydantic
             import os
             self.DATABASE_URL = os.getenv("DATABASE_URL")
             if not self.DATABASE_URL:
                 raise ValueError("DATABASE_URL environment variable is required")
    
    # Configurações JWT
    # Em produção, substitua por segredo real via env var
    JWT_SECRET_KEY: str = "1055bdc4c58da24046dcf6d2bbec3fc6f083d798e8b4e2c46bf28421dab7632b"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Carrega do arquivo .env
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

# Instância global de configurações
settings = Settings()
