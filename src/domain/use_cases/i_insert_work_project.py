from abc import ABC, abstractmethod

class IInsertWorkProject(ABC):
    
    @abstractmethod
    def insert(self, project_id:int, fiscal_id:int, title:str, description:str, photo_name:str) -> None:pass 