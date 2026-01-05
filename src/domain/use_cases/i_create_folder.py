from abc import ABC, abstractmethod

class ICreateFolder(ABC):

    @abstractmethod
    def create(self, name: str) -> None:
        '''
        Cria uma nova pasta no banco de dados

        Parâmetros:
            name: Nome da pasta que deseja inserir
        Levanta:
            FolderAlreadyExists: levanta quando a pasta que deseja inserir já existe no banco de dados
        '''

