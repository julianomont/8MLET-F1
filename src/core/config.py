"""
Configurações da aplicação.
Carrega variáveis de ambiente e define valores padrão.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

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
    DATABASE_URL: str = f"sqlite:///{BASE_DIR}/data/books.db"
    
    # Configurações JWT
    JWT_SECRET_KEY: str = "chave-secreta-desenvolvimento-altere-em-producao"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Carrega do arquivo .env
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

# Instância global de configurações
settings = Settings()
