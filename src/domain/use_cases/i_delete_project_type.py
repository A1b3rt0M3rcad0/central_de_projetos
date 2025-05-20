from abc import ABC, abstractmethod

class IDeleteProjectType(ABC):

    @abstractmethod
    def delete(self, project_id:int, type_id:int) -> None:
        '''
        deleta uma associação de tipo e empresa
        '''