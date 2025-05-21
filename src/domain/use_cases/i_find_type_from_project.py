from abc import ABC, abstractmethod
from src.domain.entities.project_types import ProjectTypeEntity
from typing import List

class IFindTypeFromProject(ABC):

    @abstractmethod 
    def find(self, project_id:int) -> List[ProjectTypeEntity]:
        '''
        Encontra o tipo do projeto
        '''