from abc import ABC, abstractmethod
from src.domain.entities.work_project import WorkProjectEntity

class IGetWorkProjectByFiscal(ABC):
    
    @abstractmethod
    def get(self, work_project_id: int, fiscal_id: int) -> WorkProjectEntity:
        """
        Busca um work project específico verificando se o fiscal está associado
        
        Args:
            work_project_id: ID do work project
            fiscal_id: ID do fiscal para verificar associação
            
        Returns:
            WorkProjectEntity: Dados do work project se o fiscal estiver associado
            
        Raises:
            WorkProjectNotExists: Se o work project não existir ou o fiscal não estiver associado
        """