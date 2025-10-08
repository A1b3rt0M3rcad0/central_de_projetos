from abc import ABC, abstractmethod

class IUpdateFiscalPhone(ABC):

    @abstractmethod
    def update(self, name: str, phone: str) -> None:
        '''
        Atualiza o telefone de um fiscal

        Parâmetros:
            name: Nome do fiscal a ser atualizado
            phone: Novo telefone do fiscal
            
        Levanta:
            FiscalNotFound: Se o fiscal não existe
        '''
        pass

