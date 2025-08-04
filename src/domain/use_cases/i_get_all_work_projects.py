from abc import ABC, abstractmethod
from typing import List
from src.domain.entities.work_project import WorkProjectEntity

class IGetAllWorkProjects(ABC):
    
    @abstractmethod
    def get_all(self) -> List[WorkProjectEntity]:pass 