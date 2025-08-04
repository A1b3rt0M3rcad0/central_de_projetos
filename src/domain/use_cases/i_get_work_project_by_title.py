from abc import ABC, abstractmethod
from src.domain.entities.work_project import WorkProjectEntity

class IGetWorkProjectByTitle(ABC):
    
    @abstractmethod
    def get_by_title(self, title:str) -> WorkProjectEntity:pass 