from abc import ABC, abstractmethod
from src.domain.entities.project_empresa import ProjectEmpresaEntity

class IFindProjectEmpresa(ABC):

    @abstractmethod
    def find(self, empresa_id:int, project_id:int) -> ProjectEmpresaEntity:
        '''
        Find project empresa
        '''