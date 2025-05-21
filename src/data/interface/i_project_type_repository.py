from abc import ABC, abstractmethod
from typing import List
from src.domain.entities.project_type import ProjectTypeEntity

class IProjectTypeRepository(ABC):

    @abstractmethod
    def insert(self, project_id: int, type_id: int) -> None:
        """Insere uma associação entre projeto e tipo"""

    @abstractmethod
    def find(self, project_id: int, type_id: int) -> ProjectTypeEntity:
        """Busca uma associação específica entre projeto e tipo"""

    @abstractmethod
    def find_all_from_type(self, type_id: int) -> List[ProjectTypeEntity]:
        """Busca todos os projetos associados a um tipo"""

    @abstractmethod
    def update_type(self, project_id: int, type_id: int, new_type_id: int) -> None:
        """Atualiza o tipo associado a um projeto"""

    @abstractmethod
    def delete(self, project_id: int, type_id: int) -> None:
        """Remove a associação entre projeto e tipo"""
    
    @abstractmethod
    def delete_all_from_project(self, project_id:int) -> None:pass

    @abstractmethod
    def select_all_from_project(self, project_id:int) -> None:pass
