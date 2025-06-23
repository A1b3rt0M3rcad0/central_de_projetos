from src.domain.entities.project_types_count_by_bairro import ProjectTypesCountByBairro
from abc import ABC, abstractmethod

class IGetProjectTypesCountByBairro(ABC):

    @abstractmethod
    def get(self) -> ProjectTypesCountByBairro:pass