from abc import ABC, abstractmethod

class IUpdateWorkProjectDescription(ABC):
    
    @abstractmethod
    def update(self, work_project_id: int, description: str) -> None: pass 