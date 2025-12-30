from abc import ABC, abstractmethod

class ICreateProjectFolder(ABC):

    @abstractmethod
    def create(self, project_id: int, folder_id: int) -> None:
        '''
        Cria uma associação do projeto à pasta

        Parâmetros:
            project_id: ID do projeto
            folder_id: ID da pasta
        Levanta:
            ProjectFolderAlreadyExists: Caso a associação de projeto-pasta já exista
        '''

