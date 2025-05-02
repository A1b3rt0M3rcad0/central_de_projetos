from abc import ABC, abstractmethod
from typing import List
from src.domain.entities.project_fiscal import ProjectFiscalEntity

class IFindAllProjectsFromFiscal(ABC):

    @abstractmethod
    def find(self, fiscal_id:int) -> List[ProjectFiscalEntity]:
        '''
        Pega todos projetos buscando pelo id do fiscal

        Parâmetros:
            fiscal_id: id do fiscal para realizar a busca
        Levanta:
            ProjectsFromFiscalDoesNotExists: Caso não exists nenhum projeto associado a um fiscal
        '''