from abc import ABC, abstractmethod

class IDeleteAssociationUserFromProject(ABC):

    @abstractmethod
    def delete(self, project_id:int) -> None:
        '''
        Delete user project association from project
        '''