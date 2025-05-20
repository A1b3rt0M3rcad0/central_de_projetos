from abc import ABC, abstractmethod

class IDeleteProjectEmpresa(ABC):

    @abstractmethod
    def delete(self, empresa_id:int, project_id:int) -> None:
        '''
        deleta a associação entre empresa e projeto
        '''