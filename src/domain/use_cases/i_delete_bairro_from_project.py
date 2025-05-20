from abc import ABC, abstractmethod

class IDeleteBairroFromProject(ABC):

    @abstractmethod
    def delete(self, project_id:int) -> None:
        '''
        Delete all project bairro association from project
        '''