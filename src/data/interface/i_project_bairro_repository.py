from abc import ABC, abstractmethod
from typing import List
from src.domain.entities.project_bairro import ProjectBairroEntity

class IProjectBairroRepository(ABC):

    @abstractmethod
    def insert(self, project_id: int, bairro_id: int) -> None:
        """Insere uma nova associação entre projeto e bairro"""

    @abstractmethod
    def find(self, project_id: int, bairro_id: int) -> ProjectBairroEntity:
        """Busca uma associação específica entre projeto e bairro"""

    @abstractmethod
    def find_all_from_bairro(self, bairro_id: int) -> List[ProjectBairroEntity]:
        """Busca todos os projetos associados a um bairro"""

    @abstractmethod
    def update_bairro(self, project_id: int, bairro_id: int, new_bairro_id: int) -> None:
        """Atualiza a associação do bairro em um projeto"""

    @abstractmethod
    def delete(self, project_id: int, bairro_id: int) -> None:
        """Deleta a associação entre projeto e bairro"""