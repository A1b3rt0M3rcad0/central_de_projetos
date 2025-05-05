from abc import ABC, abstractmethod

class ICreateProjectBairro(ABC):

    @abstractmethod
    def create(self, project_id:int, bairro_id:int) -> None:
        '''
        Cria uma associação do projeto ao bairro

        Parãmetros:
            project_id: ID do projeto
            bairro_id: ID do bairro
        Levanta:
            ProjectBairroAlreadyExists: Caso a associação de projeto bairro ja exista
        '''