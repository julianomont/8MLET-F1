"""
Ponto de entrada principal da API FastAPI.
"""
from fastapi import FastAPI
from src.api.v1.router import api_router
from src.core.config import settings
from src.core.database import engine, Base, SessionLocal
from src.models.book import BookModel
from src.core.logging import logger
from src.core.middleware import LoggingMiddleware

# Cria a instância do FastAPI com configurações
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="""
## API de Livros

Esta API fornece acesso a uma base de dados de livros extraídos via web scraping do site https://books.toscrape.com/.

### Tech Challenge - Fase 1  - PosTech 8MLET
- **Por Juliano Monteiro (rm369594)**
- **GitHub:** https://github.com/julianomont
- **Email:** juliano.monteiro@outlook.com
- **LinkedIn:** https://www.linkedin.com/in/julianofmonteiro

### Funcionalidades:
- **Listagem e busca** de livros com paginação
- **Filtros** por título, categoria e faixa de preço
- **Estatísticas** gerais e por categoria
- **Features para ML** prontas para treinamento de modelos
- **Autenticação JWT** para rotas protegidas
- **Métricas de performance** via /api/v1/metrics


### Segurança
- **Autenticação JWT** 
- **Login:** admin
- **Senha:** admin-8MLET

### Documentação
- **Documentação:** via /docs
- **Documentação:** via /redoc

### Métricas
- **Métricas de performance** via /api/v1/metrics

    """,
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    debug=settings.DEBUG
)

# Adiciona middleware de logging e métricas
app.add_middleware(LoggingMiddleware)

# Registra as rotas da API v1
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.on_event("startup")
async def startup_event():
    """Evento executado ao iniciar a aplicação."""
    logger.info("Iniciando Books API...")
    try:

        # Cria as tabelas no banco de dados
        Base.metadata.create_all(bind=engine)
        
        # Garante que o usuário admin existe
        from src.services.auth_service import ensure_admin_user
        db = SessionLocal()
        try:
            ensure_admin_user(db)
        finally:
            db.close()
        logger.info("Inicialização do banco de dados e seeding concluídos.")
    except Exception as e:
        logger.error(f"Erro durante a inicialização do banco: {e}")
        logger.warning("A aplicação continuará subindo para responder ao health check.")

    logger.info("Books API pronta e ouvindo.")

@app.get("/", tags=["Raiz"], summary="Página inicial", description="Retorna mensagem de boas-vindas")
def root():
    """Rota raiz - retorna mensagem de boas-vindas."""
    return {"message": "Bem-vindo à Books API. Visite /docs para documentação."}

