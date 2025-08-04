from abc import ABC, abstractmethod
from typing import Dict

class IUpdateWorkProject(ABC):
    
    @abstractmethod
    def update(self, work_project_id:int, update_params:Dict) -> None:pass 