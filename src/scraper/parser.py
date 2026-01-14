"""
Parser de livros.
Extrai dados estruturados do HTML.
"""
from bs4 import BeautifulSoup
import re
from src.schemas.responses import BookBase as Book
from src.core.logging import logger

class BookParser:
    """Classe para analisar HTML e extrair dados de livros."""
    
    # Mapeamento de texto para valor numérico da avaliação
    # Os valores em inglês (One, Two, etc.) vêm do site fonte
    RATING_MAP = {
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5
    }

    @staticmethod
    def parse_book_item(html_soup, category: str) -> Book:
        """Extrai dados de um item de livro do HTML."""
        try:
            # Extrai título
            title = html_soup.h3.a["title"]
            
            # Extrai e normaliza preço
            price_text = html_soup.find("p", class_="price_color").text
            price = float(re.sub(r"[^\d.]", "", price_text))
            
            # Extrai avaliação
            rating_class = html_soup.find("p", class_="star-rating")["class"][1]
            rating = BookParser.RATING_MAP.get(rating_class, 0)
            
            # Verifica disponibilidade (texto em inglês vem do site fonte)
            availability_text = html_soup.find("p", class_="instock availability").text.strip()
            availability = "In stock" in availability_text
            
            # Monta URL da imagem
            image_src = html_soup.find("img", class_="thumbnail")["src"]
            image_url = f"http://books.toscrape.com/{image_src.replace('../', '')}"
            
            return Book(
                title=title,
                price=price,
                rating=rating,
                availability=availability,
                category=category,
                image_url=image_url
            )
        except Exception as e:
            logger.error(f"Erro ao processar item do livro: {e}")
            raise
