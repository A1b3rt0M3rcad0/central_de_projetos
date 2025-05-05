from src.domain.entities.empresa import EmpresaEntity
from abc import ABC, abstractmethod

class IFindEmpresaByExactName(ABC):

    @abstractmethod
    def find(self, name:str) -> EmpresaEntity:
        '''
        Encontra uma empresa pelo seu nome exato

        Parâmetros:
            name: Nome da empresa
        Levanta:
            EmpresaNotExists: caso não encotnre nenhuma empresa com esse nome
        '''