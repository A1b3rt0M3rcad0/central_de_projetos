from abc import ABC, abstractmethod
from src.domain.entities.project_folder import ProjectFolderEntity
from typing import List

class IFindAllProjectsFromFolder(ABC):

    @abstractmethod
    def find(self, folder_id: int) -> List[ProjectFolderEntity]:
        '''
        Encontra todos os projetos associados a uma pasta

        Parâmetros:
            folder_id: ID da pasta
        Retorna:
            Lista de ProjectFolderEntity
        '''

