from src.domain.entities.project_bairro_verba_summary import ProjectBairroVerbaSummary
from abc import ABC, abstractmethod

class IGetProjectVerbaByBairro(ABC):

    @abstractmethod
    def get(self) -> ProjectBairroVerbaSummary:pass