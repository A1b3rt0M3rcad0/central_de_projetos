from abc import ABC, abstractmethod

class IDeleteProjectFolder(ABC):

    @abstractmethod
    def delete(self, project_id: int, folder_id: int) -> None:
        '''
        Remove a associação entre projeto e pasta

        Parâmetros:
            project_id: ID do projeto
            folder_id: ID da pasta
        Levanta:
            ProjectFolderNotExists: Caso não encontre a associação
        '''

