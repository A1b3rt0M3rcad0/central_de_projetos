from abc import ABC, abstractmethod
from src.domain.entities.work_project import WorkProjectEntity

class IGetWorkProject(ABC):
    
    @abstractmethod
    def get(self, work_project_id:int) -> WorkProjectEntity:pass 