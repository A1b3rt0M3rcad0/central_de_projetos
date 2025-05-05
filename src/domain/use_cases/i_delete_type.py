from abc import ABC, abstractmethod

class IDeleteType(ABC):

    @abstractmethod
    def delete(self, name:str) -> None:
        '''
        Deleta um typo pelo nome dele

        Parâmetros:
            name: Nome do type que deseja ser deletado
        Levanta:
            None
        '''