from abc import ABC, abstractmethod
from typing import Dict, Union
from src.domain.entities.project import ProjectEntity

class IGetProjectsWithPagination(ABC):

    @abstractmethod
    def get(self, page:int, page_size:int=10) -> Dict[str, Union[int, ProjectEntity]]:pass