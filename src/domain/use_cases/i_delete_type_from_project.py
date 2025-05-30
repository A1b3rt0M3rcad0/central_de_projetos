from abc import ABC, abstractmethod

class IDeleteTypeFromProject(ABC):

    @abstractmethod
    def delete(self, project_id:int) -> None:
        '''
        Delete all project type association from project
        '''