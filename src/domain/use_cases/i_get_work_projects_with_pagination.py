from abc import ABC, abstractmethod
from typing import Dict, Union, List
from src.domain.entities.work_project import WorkProjectEntity

class IGetWorkProjectsWithPagination(ABC):
    
    @abstractmethod
    def get_with_pagination(self, page:int, page_size:int) -> Dict[str, Union[int, List[WorkProjectEntity]]]:pass 