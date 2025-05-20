from abc import ABC, abstractmethod
from src.domain.entities.project_empresa import ProjectEmpresaEntity
from typing import List

class IFindAllProjectsfromEmpresa(ABC):

    @abstractmethod
    def find(self, empresa_id:int) -> List[ProjectEmpresaEntity]:
        '''
        Find all projects from empresa
        '''