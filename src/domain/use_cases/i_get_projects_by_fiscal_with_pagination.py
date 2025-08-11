from abc import ABC, abstractmethod
from typing import Dict, Union, List
from src.domain.entities.project_fiscal import ProjectFiscalEntity

class IGetProjectsByFiscalWithPagination(ABC):

    @abstractmethod
    def get(self, fiscal_id: int, page: int, page_size: int = 10) -> Dict[str, Union[int, List[ProjectFiscalEntity]]]:
        """
        Retorna projetos associados a um fiscal com paginação
        
        Parâmetros:
            fiscal_id: ID do fiscal
            page: Número da página
            page_size: Tamanho da página
            
        Retorna:
            Dicionário com informações de paginação e lista de projetos
        """