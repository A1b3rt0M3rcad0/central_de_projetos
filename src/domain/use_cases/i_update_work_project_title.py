from abc import ABC, abstractmethod

class IUpdateWorkProjectTitle(ABC):
    
    @abstractmethod
    def update(self, work_project_id: int, title: str) -> None: pass 