from abc import ABC, abstractmethod

class ICreateProjectEmpresa(ABC):

    @abstractmethod
    def create(self,empresa_id:int, project_id:int) -> None:
        '''
        Create empresa project association
        '''