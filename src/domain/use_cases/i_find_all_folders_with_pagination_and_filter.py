from abc import ABC, abstractmethod
from src.domain.entities.folder import FolderEntity
from typing import List

class IFindAllFoldersWithPaginationAndFilter(ABC):

    @abstractmethod
    def find(self, page: int, page_size: int, search_term: str = None) -> List[FolderEntity]:
        '''
        Retorna todas as pastas com paginação e filtro global

        Parâmetros:
            page: número da página (começando em 1)
            page_size: quantidade de itens por página
            search_term: termo de busca opcional para filtrar por nome
        Retorna:
            Lista de FolderEntity
        '''

