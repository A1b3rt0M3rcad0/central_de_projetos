from abc import ABC, abstractmethod
from src.domain.entities.folder import FolderEntity
from typing import List

class IFindAllFolder(ABC):

    @abstractmethod
    def find(self) -> List[FolderEntity]:
        '''
        Retorna todas as pastas do banco de dados

        Retorna:
            Lista de FolderEntity
        '''

