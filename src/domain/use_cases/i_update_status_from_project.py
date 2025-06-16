from abc import ABC, abstractmethod

class IUpdateStatusFromProject(ABC):

    @abstractmethod
    def update(self, project_id:int, status_id:int) -> None:
        pass