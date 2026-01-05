from abc import ABC, abstractmethod
from typing import Dict, Any

class IGetProjectsWithPaginationAndFilter(ABC):
    """
    Interface para buscar projetos com paginação e filtro global.
    """

    @abstractmethod
    def get(self, page_size: int, page: int, search_term: str = None) -> Dict[str, Any]:
        """
        Busca projetos com paginação e filtro opcional.

        Args:
            page_size: Número de itens por página
            page: Número da página (baseado em 1)
            search_term: Termo de busca opcional para filtrar projetos

        Returns:
            Dict contendo:
                - projects: Lista de projetos da página atual
                - total_items: Total de projetos no sistema (com filtro aplicado)
                - total_pages: Total de páginas
                - current_page: Página atual
                - page_size: Tamanho da página

        Raises:
            ProjectsNotFoundError: Se nenhum projeto for encontrado
            InvalidPaginationError: Se os parâmetros de paginação forem inválidos
            InternalServerError: Para outros erros internos
        """
        pass
