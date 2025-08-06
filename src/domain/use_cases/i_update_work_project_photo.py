from abc import ABC, abstractmethod

class IUpdateWorkProjectPhoto(ABC):
    
    @abstractmethod
    def update(self, work_project_id: int, photo_name: str) -> None: pass 