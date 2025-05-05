from abc import ABC, abstractmethod
from typing import List
from src.domain.entities.project_bairro import ProjectBairroEntity

class IFindAllProjectsFromBairro(ABC):

    @abstractmethod
    def find(self, bairro_id:int) -> List[ProjectBairroEntity]:
        '''
        Encontra todos os projetos realizados no bairro

        Parãmetros:
            bairro_id: ID do bairro
        Levanta:
            ProjectsFromBairroDoesNotExists: Caso não encontre nehnum projeto associado ao bairro
        '''