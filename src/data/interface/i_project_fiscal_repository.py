from abc import ABC, abstractmethod
from typing import List
from src.domain.entities.project_fiscal import ProjectFiscalEntity

class IProjectFiscalRepository(ABC):

    @abstractmethod
    def insert(self, project_id: int, fiscal_id: int) -> None:
        """Insere uma nova associação entre um projeto e um fiscal"""

    @abstractmethod
    def find_all_from_fiscal(self, fiscal_id: int) -> List[ProjectFiscalEntity]:
        """Retorna todos os projetos associados a um fiscal"""

    @abstractmethod
    def find(self, fiscal_id: int, project_id: int) -> ProjectFiscalEntity:
        """Busca uma associação específica entre projeto e fiscal"""

    @abstractmethod
    def update_fiscal(self, project_id: int, fiscal_id: int, new_fiscal_id: int) -> None:
        """Atualiza o fiscal responsável por um projeto"""

    @abstractmethod
    def delete(self, project_id: int, fiscal_id: int) -> None:
        """Remove a associação entre um projeto e um fiscal"""