from abc import ABC, abstractmethod
from src.domain.entities.folder import FolderEntity
from typing import List

class IFindAllFoldersWithPagination(ABC):

    @abstractmethod
    def find(self, page: int, page_size: int) -> List[FolderEntity]:
        '''
        Retorna todas as pastas com paginação

        Parâmetros:
            page: número da página (começando em 1)
            page_size: quantidade de itens por página
        Retorna:
            Lista de FolderEntity
        '''

