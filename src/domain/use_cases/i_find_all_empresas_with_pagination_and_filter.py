from abc import ABC, abstractmethod
from typing import Dict, Any

class IFindAllEmpresasWithPaginationAndFilter(ABC):
    """
    Interface para buscar todas as empresas com paginação e filtro global.
    """

    @abstractmethod
    def find(self, page_size: int, page: int, search_term: str = None) -> Dict[str, Any]:
        """
        Busca todas as empresas com paginação e filtro opcional.

        Args:
            page_size: Número de itens por página
            page: Número da página (baseado em 1)
            search_term: Termo de busca opcional para filtrar empresas

        Returns:
            Dict contendo:
                - empresas: Lista de empresas da página atual
                - total_items: Total de empresas no sistema (com filtro aplicado)
                - total_pages: Total de páginas
                - current_page: Página atual
                - page_size: Tamanho da página

        Raises:
            EmpresasNotFoundError: Se nenhuma empresa for encontrada
            InvalidPaginationError: Se os parâmetros de paginação forem inválidos
            InternalServerError: Para outros erros internos
        """
        pass
