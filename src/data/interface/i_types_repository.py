from abc import ABC, abstractmethod
from src.domain.entities.types import TypesEntity
from typing import List


class ITypesRepository(ABC):

    @abstractmethod
    def insert(self, name: str) -> None:
        """Insere um novo tipo no banco de dados."""

    @abstractmethod
    def find_by_name(self, name: str) -> TypesEntity:
        """Busca um tipo pelo nome e retorna a entidade correspondente."""
    
    @abstractmethod
    def find_all(self) -> List[TypesEntity]:
        '''Busca todos os tipos e retorna uma lista de entidade'''

    @abstractmethod
    def update(self, name: str, new_name: str) -> None:
        """Atualiza o nome de um tipo existente."""

    @abstractmethod
    def delete(self, name: str) -> None:
        """Deleta um tipo com base no nome."""