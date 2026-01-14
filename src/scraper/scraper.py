"""
Scraper de livros.
Extrai dados do site books.toscrape.com.
Navega por todas as categorias para capturar todos os livros.
"""
import httpx
import asyncio
from typing import List, Dict
from bs4 import BeautifulSoup
from src.scraper.parser import BookParser
from src.schemas.responses import BookBase as Book
from src.core.config import settings
from src.core.logging import logger


class BookScraper:
    """Classe para fazer scraping robusto de livros."""
    
    def __init__(self):
        """Inicializa o scraper com URL base e parser."""
        self.base_url = settings.SCRAPE_URL
        self.parser = BookParser()

    async def fetch_page(self, client: httpx.AsyncClient, url: str) -> str:
        """Busca o conteúdo HTML de uma página com retry."""
        for attempt in range(settings.MAX_RETRIES):
            try:
                response = await client.get(url, timeout=10.0)
                response.raise_for_status()
                return response.text
            except Exception as e:
                logger.warning(f"Tentativa {attempt + 1} falhou para {url}: {e}")
                if attempt == settings.MAX_RETRIES - 1:
                    raise
                await asyncio.sleep(settings.RETRY_DELAY)
        return ""

    async def get_categories(self, client: httpx.AsyncClient) -> Dict[str, str]:
        """Extrai todas as categorias disponíveis no site."""
        categories = {}
        try:
            content = await self.fetch_page(client, self.base_url)
            soup = BeautifulSoup(content, "html.parser")
            
            # Encontra a sidebar de categorias
            category_list = soup.find("ul", class_="nav-list")
            if category_list:
                # Pula o primeiro item (Books - categoria pai)
                cat_items = category_list.find_all("li")[1:]
                for item in cat_items:
                    link = item.find("a")
                    if link:
                        cat_name = link.text.strip()
                        cat_url = self.base_url + "/" + link["href"]
                        categories[cat_name] = cat_url
                        
            logger.info(f"Encontradas {len(categories)} categorias")
        except Exception as e:
            logger.error(f"Erro ao extrair categorias: {e}")
        
        return categories

    async def scrape_category(self, client: httpx.AsyncClient, category: str, category_url: str) -> List[Book]:
        """Extrai todos os livros de uma categoria específica."""
        books = []
        current_url = category_url
        page = 1
        
        while current_url:
            try:
                content = await self.fetch_page(client, current_url)
                soup = BeautifulSoup(content, "html.parser")
                
                # Processa cada livro na página
                items = soup.find_all("article", class_="product_pod")
                for item in items:
                    book = self.parser.parse_book_item(item, category=category)
                    books.append(book)
                
                # Verifica se há próxima página
                next_button = soup.find("li", class_="next")
                if next_button:
                    next_link = next_button.find("a")["href"]
                    # Constrói URL da próxima página
                    base_cat_url = current_url.rsplit("/", 1)[0]
                    current_url = f"{base_cat_url}/{next_link}"
                    page += 1
                else:
                    current_url = None
                    
            except Exception as e:
                logger.error(f"Erro ao raspar {category} página {page}: {e}")
                break
                
        return books

    async def scrape_all(self) -> List[Book]:
        """
        Extrai todos os livros disponíveis no site.
        Navega por cada categoria para garantir a captura completa.
        
        Campos capturados:
        - título
        - preço
        - rating (1-5)
        - disponibilidade
        - categoria
        - imagem
        """
        all_books = []
        
        async with httpx.AsyncClient() as client:
            # Obtém todas as categorias
            categories = await self.get_categories(client)
            
            if not categories:
                # Fallback: raspa sem categorias
                logger.warning("Nenhuma categoria encontrada, usando método fallback")
                return await self._scrape_fallback(client)
            
            # Raspa cada categoria
            for category, url in categories.items():
                logger.info(f"Raspando categoria: {category}")
                category_books = await self.scrape_category(client, category, url)
                all_books.extend(category_books)
                logger.info(f"  → {len(category_books)} livros extraídos de '{category}'")
                
                # Pequeno delay entre categorias para não sobrecarregar o servidor
                await asyncio.sleep(0.5)
        
        logger.info(f"Total de livros extraídos: {len(all_books)}")
        return all_books

    async def _scrape_fallback(self, client: httpx.AsyncClient) -> List[Book]:
        """Método fallback que raspa todas as páginas sem categoria específica."""
        all_books = []
        current_url = self.base_url + "/catalogue/page-1.html"
        page = 1
        
        while current_url:
            logger.info(f"Raspando página {page}...")
            try:
                content = await self.fetch_page(client, current_url)
                soup = BeautifulSoup(content, "html.parser")
                
                items = soup.find_all("article", class_="product_pod")
                for item in items:
                    book = self.parser.parse_book_item(item, category="Geral")
                    all_books.append(book)
                
                next_button = soup.find("li", class_="next")
                if next_button and page < 50:
                    page += 1
                    current_url = self.base_url + f"/catalogue/page-{page}.html"
                else:
                    current_url = None
                    
            except Exception as e:
                logger.error(f"Falha ao raspar página {page}: {e}")
                break
                
        return all_books

