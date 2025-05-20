from abc import ABC, abstractmethod
from typing import List
from src.domain.entities.project_empresa import ProjectEmpresaEntity


class IProjectEmpresaRepository(ABC):

    @abstractmethod
    def insert(self, project_id: int, empresa_id: int) -> None:
        """Insere uma associação entre projeto e empresa"""

    @abstractmethod
    def find(self, project_id: int, empresa_id: int) -> ProjectEmpresaEntity:
        """Busca uma associação específica entre projeto e empresa"""

    @abstractmethod
    def find_all_from_empresa(self, empresa_id: int) -> List[ProjectEmpresaEntity]:
        """Busca todas as associações de um empresa_id"""

    @abstractmethod
    def update_empresa(self, project_id: int, empresa_id: int, new_empresa_id: int) -> None:
        """Atualiza o empresa_id de uma associação existente"""

    @abstractmethod
    def delete(self, project_id: int, empresa_id: int) -> None:
        """Remove uma associação entre projeto e empresa"""
    
    @abstractmethod
    def delete_all_from_project(self, project_id:int) -> None:pass
