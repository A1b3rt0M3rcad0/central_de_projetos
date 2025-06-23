from abc import ABC, abstractmethod
from src.domain.entities.project_bairro_status_summary import ProjectBairroStatusSummary

class IGetProjectStatusCountByBairro(ABC):

    @abstractmethod
    def get(self) -> ProjectBairroStatusSummary:pass