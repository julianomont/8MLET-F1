"""
Repositório base abstrato.
Define a interface que todos os repositórios devem implementar.
"""
from abc import ABC, abstractmethod
from typing import List, Optional, Generic, TypeVar

T = TypeVar("T")

class BaseRepository(ABC, Generic[T]):
    """Interface base para repositórios."""
    
    @abstractmethod
    def get_all(self) -> List[T]:
        """Retorna todos os registros."""
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[T]:
        """Busca um registro pelo ID."""
        pass

    @abstractmethod
    def find(self, **kwargs) -> List[T]:
        """Busca registros com filtros."""
        pass
