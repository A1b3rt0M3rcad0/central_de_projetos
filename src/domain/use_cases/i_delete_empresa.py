from abc import ABC, abstractmethod

class IDeleteEmpresa(ABC):

    @abstractmethod
    def delete(self, name:str) -> None:
        '''
        Delete uma empresa

        Parâmetros:
            name: nome da empresa
        Levanta:
            None
        '''