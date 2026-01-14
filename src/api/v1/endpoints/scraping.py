"""
Endpoint de scraping (protegido).
Permite disparo manual do processo de scraping apenas por administradores.
"""
from fastapi import APIRouter, Depends, BackgroundTasks
from src.api.deps import get_current_admin_user
from src.models.user import UserModel
from src.core.logging import logger

router = APIRouter()


@router.post(
    "/trigger",
    summary="Disparar Scraping",
    description="Inicia o processo de scraping de livros. Requer autenticação de admin."
)
def trigger_scraping(
    background_tasks: BackgroundTasks,
    current_user: UserModel = Depends(get_current_admin_user)
):
    """
    Dispara o processo de scraping em background.
    
    Apenas usuários administradores podem executar esta ação.
    O scraping é executado de forma assíncrona em background.
    """
    # Importa aqui para evitar dependência circular
    from src.scraper.scraper import BookScraper
    from src.scraper.exporter import DataExporter
    
    def run_scraping():
        """Executa o scraping em background."""
        try:
            logger.info(f"Scraping iniciado pelo usuário: {current_user.username}")
            scraper = BookScraper()
            # O método scrape_all é assíncrono, precisamos executá-lo
            import asyncio
            books = asyncio.run(scraper.scrape_all())
            
            exporter = DataExporter()
            exporter.export_to_db(books)
            logger.info(f"Scraping concluído. {len(books)} livros extraídos.")
        except Exception as e:
            logger.error(f"Erro durante scraping: {str(e)}")
    
    background_tasks.add_task(run_scraping)
    
    return {
        "message": "Scraping iniciado em background",
        "triggered_by": current_user.username
    }
