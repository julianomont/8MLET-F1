"""
Configuração de logging da aplicação.
"""
import logging
import sys

def setup_logging():
    """Configura o sistema de logs."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )

# Logger principal da aplicação
logger = logging.getLogger("books-api")
setup_logging()
