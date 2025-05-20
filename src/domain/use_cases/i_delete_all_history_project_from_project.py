from abc import ABC, abstractmethod

class IDeleteAllHistoryProjectFromProject(ABC):

    @abstractmethod
    def delete(self, project_id:int) -> None:
        '''
        Delete all history project association from project
        '''