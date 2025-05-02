from abc import ABC, abstractmethod
from src.domain.entities.project_fiscal import ProjectFiscalEntity

class IFindProjectFiscal(ABC):

    @abstractmethod
    def find(self, project_id:int, fiscal_id:int) -> ProjectFiscalEntity:
        '''
        Encontra um ProjectFiscal especiaco, ou seja uma associação de projeto fiscal especifica
        
        Parâmetros:
            project_id: ID do projeto
            fiscal_id: ID do fiscal
        Levanta:
            ProjectsFromFiscalDoesNotExists: caso não exista essa associação de projeto fical
        '''