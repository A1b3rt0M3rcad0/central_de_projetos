from abc import ABC, abstractmethod

class IDeleteWorkProject(ABC):

    @abstractmethod
    def delete(self, work_project_id:int) -> None:pass 