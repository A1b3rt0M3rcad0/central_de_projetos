from abc import ABC, abstractmethod

class IDeleteFiscal(ABC):

    @abstractmethod
    def delete(self, name:str) -> None:
        '''
        Realiza a deleção do fiscal no banco de dados

        Parâmetros:
            name: nome do fiscal que ira ser deletado
        Levanta:
            ErrorOnDeleteFiscal: Levanta esse erro quando ouver qualquer problema ao se deletar o fiscal
        '''