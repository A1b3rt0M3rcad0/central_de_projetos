from abc import ABC, abstractmethod

class IDeleteBairro(ABC):

    @abstractmethod
    def delete(self, name:str) -> None:
        '''
        Delete o bairro pelo nome exato

        Parãmetros:
            name: nome do bairro
        Levanta:
            Exception
        '''