from abc import ABC, abstractmethod
from src.domain.entities.folder import FolderEntity

class IFindFolderById(ABC):

    @abstractmethod
    def find(self, folder_id: int) -> FolderEntity:
        '''
        Retorna a pasta pelo id

        Parâmetros:
            folder_id: id da pasta
        Levanta:
            FolderNotExists: caso não encontre nenhuma pasta
        '''

