from abc import ABC, abstractmethod
from src.domain.entities.project_bairro_summary import ProjectBairroSummary

class IGetProjectCountsByBairro(ABC):

    @abstractmethod
    def get(self) -> ProjectBairroSummary:pass