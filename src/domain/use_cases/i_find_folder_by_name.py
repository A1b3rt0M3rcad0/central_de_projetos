from abc import ABC, abstractmethod
from src.domain.entities.folder import FolderEntity
from typing import Optional

class IFindFolderByName(ABC):

    @abstractmethod
    def find(self, name: str) -> Optional[FolderEntity]:
        '''
        Retorna a pasta pelo nome

        Parâmetros:
            name: nome da pasta
        Retorna:
            FolderEntity se encontrada, None caso contrário
        '''

