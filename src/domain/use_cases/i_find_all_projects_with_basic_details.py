from src.domain.entities.project import ProjectEntity
from typing import List
from abc import ABC, abstractmethod

class IFindAllProjectsWithBasicDetails(ABC):

    @abstractmethod
    def find(self) -> List[ProjectEntity]:
        """Retorna uma lista com todas as entidades deprojetos com detalhes basicos"""