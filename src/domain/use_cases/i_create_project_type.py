from abc import ABC, abstractmethod

class ICreateProjectType(ABC):

    @abstractmethod
    def create(self, project_id:int, type_id:int) -> None:
        '''
        Cria uma associação de projeto e tipo
        '''