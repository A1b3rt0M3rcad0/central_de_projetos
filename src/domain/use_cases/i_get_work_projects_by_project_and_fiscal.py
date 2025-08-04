from abc import ABC, abstractmethod
from typing import List
from src.domain.entities.work_project import WorkProjectEntity

class IGetWorkProjectsByProjectAndFiscal(ABC):
    
    @abstractmethod
    def get_by_project_and_fiscal(self, project_id:int, fiscal_id:int) -> List[WorkProjectEntity]:pass 