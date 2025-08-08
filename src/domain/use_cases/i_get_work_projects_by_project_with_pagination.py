from abc import ABC, abstractmethod
from typing import Dict, Union, List
from src.domain.entities.work_project import WorkProjectEntity

class IGetWorkProjectsByProjectWithPagination(ABC):
    
    @abstractmethod
    def get_by_project_with_pagination(self, project_id:int, page:int, page_size:int) -> Dict[str, Union[int, List[WorkProjectEntity]]]:pass 