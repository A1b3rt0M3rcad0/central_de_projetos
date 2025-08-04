from abc import ABC, abstractmethod
from typing import List
from src.domain.entities.work_project import WorkProjectEntity

class IGetWorkProjectsByFiscal(ABC):
    
    @abstractmethod
    def get_by_fiscal(self, fiscal_id:int) -> List[WorkProjectEntity]:pass 