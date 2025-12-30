from abc import ABC, abstractmethod
from src.domain.entities.project_folder import ProjectFolderEntity

class IFindProjectFolder(ABC):

    @abstractmethod
    def find(self, project_id: int, folder_id: int) -> ProjectFolderEntity:
        '''
        Busca uma associação específica entre projeto e pasta

        Parâmetros:
            project_id: ID do projeto
            folder_id: ID da pasta
        Levanta:
            ProjectFolderNotExists: Caso não encontre a associação
        '''

