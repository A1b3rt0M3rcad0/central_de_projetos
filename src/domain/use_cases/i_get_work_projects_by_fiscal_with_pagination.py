from abc import ABC, abstractmethod
from typing import Dict, Union, List
from src.domain.entities.work_project import WorkProjectEntity

class IGetWorkProjectsByFiscalWithPagination(ABC):
    
    @abstractmethod
    def get_by_fiscal_with_pagination(self, fiscal_id:int, page:int, page_size:int) -> Dict[str, Union[int, List[WorkProjectEntity]]]:pass 