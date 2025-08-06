from abc import ABC, abstractmethod

class IUpdateWorkProjectDocuments(ABC):
    
    @abstractmethod
    def update(self, work_project_id: int, additional_documents: str) -> None: pass 