from abc import ABC, abstractmethod
from src.domain.entities.project_folder import ProjectFolderEntity
from typing import List

class IFindAllFoldersFromProject(ABC):

    @abstractmethod
    def find(self, project_id: int) -> List[ProjectFolderEntity]:
        '''
        Encontra todas as pastas associadas a um projeto

        Parâmetros:
            project_id: ID do projeto
        Retorna:
            Lista de ProjectFolderEntity
        '''

