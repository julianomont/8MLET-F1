"""
Script para executar o pipeline de scraping.
Extrai livros do site e salva no banco de dados.
"""
import asyncio
import sys
import os

# Adiciona src ao path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.scraper.scraper import BookScraper
from src.scraper.exporter import DataExporter
from src.core.logging import logger

async def run():
    """Executa o pipeline de scraping."""
    logger.info("Iniciando Pipeline de Scraping...")
    scraper = BookScraper()
    try:
        # Extrai livros do site
        books = await scraper.scrape_all()
        logger.info(f"Raspagem concluída com sucesso: {len(books)} livros.")
        
        # Salva no banco de dados
        exporter = DataExporter()
        exporter.export_to_db(books)
        
    except Exception as e:
        logger.error(f"Pipeline falhou: {e}")

if __name__ == "__main__":
    asyncio.run(run())
