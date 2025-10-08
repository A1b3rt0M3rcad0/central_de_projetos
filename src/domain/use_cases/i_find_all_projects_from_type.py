from abc import ABC, abstractmethod
from src.domain.entities.project_type import ProjectTypeEntity
from typing import List

class IFindAllProjectsFromType(ABC):

    @abstractmethod
    def find(self, type_id: int) -> List[ProjectTypeEntity]:
        '''
        Busca todos os projetos associados a um tipo específico

        Parâmetros:
            type_id: ID do tipo
            
        Retorna:
            Lista de ProjectTypeEntity
            
        Levanta:
            ProjectTypeNotExists: Se não houver projetos com este tipo
        '''
        pass

