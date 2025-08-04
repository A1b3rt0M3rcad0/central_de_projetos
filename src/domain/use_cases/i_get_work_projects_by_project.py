from abc import ABC, abstractmethod
from typing import List
from src.domain.entities.work_project import WorkProjectEntity

class IGetWorkProjectsByProject(ABC):
    
    @abstractmethod
    def get_by_project(self, project_id:int) -> List[WorkProjectEntity]:pass 