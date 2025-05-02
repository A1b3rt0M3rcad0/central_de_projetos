from abc import ABC, abstractmethod

class ICreateBairro(ABC):

    @abstractmethod
    def create(self, name:str) -> None:
        '''
        Crie um novo bairro no banco de dados

        Parãmetros:
            name: Nome do bairro que deseja inserir
        Levanta:
            BairroAlreadyExists: levanta quanto o bairro que deseja inserir ja existe no banco de dados
        '''