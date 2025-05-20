from abc import ABC, abstractmethod

class IDeleteEmpresaFromProject(ABC):

    @abstractmethod
    def delete(self, project_id:int) -> None:
        '''
        Delete all project empresa association from project
        '''