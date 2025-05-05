from abc import ABC, abstractmethod

class IUpdateEmpresa(ABC):

    @abstractmethod
    def update(self, name:str, new_name:str) -> None:
        '''
        Realiza o update do nome da empresa no banco de dados

        Parâmetros:
            name: nome da empresa em que deseja fazer o update do nome
            new_name: nome atualizado da empresas
        '''