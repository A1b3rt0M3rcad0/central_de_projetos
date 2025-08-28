#pylint:disable=all
from abc import ABC, abstractmethod
from typing import Optional
from src.domain.entities.work_project import WorkProjectEntity

class IGetLatestWorkProjectByProject(ABC):
    
    @abstractmethod
    def get_latest_by_project(self, project_id: int) -> Optional[WorkProjectEntity]:
        """
        Retorna o último work project criado para um projeto específico.
        
        Parâmetros:
            project_id: ID do projeto para o qual buscar o último work project
            
        Retorno:
            WorkProjectEntity ou None se não houver work projects para o projeto
            
        Levanta:
            InternalServerError: Para qualquer erro durante a operação
        """
        pass 