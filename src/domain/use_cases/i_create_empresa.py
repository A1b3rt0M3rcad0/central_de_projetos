from abc import ABC, abstractmethod

class ICreateEmpresa(ABC):

    @abstractmethod
    def create(self, name:str) -> None:
        '''
        Crie uma empresa pelo nome

        Parâmetros:
            name: Nome da empresa
        Levanta:
            EmpresaAlreadyExists: Caso a empresa com esse nome ja exista no banco de dados
        '''