from abc import ABC, abstractmethod

class IUpdateFiscalName(ABC):

    @abstractmethod
    def update(self, name:str, new_name:str) -> None:
        '''
        Realiza o update do nome do fiscal

        Parâmetros:
            name: Antigo nome do fiscal, mas realizar a busca
            new_name: Novo nome do fiscal que sera modificado
        Levanta:
            ErrorOnUpdateFiscalName: Levanta esse erro quando der qualquer problema ao realizar o update do nome do fiscal
        '''