from abc import ABC, abstractmethod

class IDeleteFiscalFromProject(ABC):

    @abstractmethod
    def delete(self, project_id:int) -> None:
        '''
        Delete all project fiscal association from project
        '''