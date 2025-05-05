from abc import ABC, abstractmethod

class ICreateType(ABC):

    @abstractmethod
    def create(self, name:str) -> None:
        '''
        Cria um typo de projeto

        Parâmetros:
            name; nome do typo
        Levanta:
            TypesAlreadyExists: caso ja exista um tipo com esse nome
        '''