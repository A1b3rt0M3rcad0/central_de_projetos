from abc import ABC, abstractmethod
from typing import Dict, Any

class IFindAllStatusWithPaginationAndFilter(ABC):
    """
    Interface para buscar todos os status com paginação e filtro global.
    """

    @abstractmethod
    def find(self, page_size: int, page: int, search_term: str = None) -> Dict[str, Any]:
        """
        Busca todos os status com paginação e filtro global.

        Args:
            page_size: Número de itens por página
            page: Número da página (baseado em 1)
            search_term: Termo de busca opcional para filtrar status

        Returns:
            Dict contendo:
                - status: Lista de status da página atual
                - total_items: Total de status no sistema (com filtro aplicado)
                - total_pages: Total de páginas
                - current_page: Página atual
                - page_size: Tamanho da página

        Raises:
            StatusNotFoundError: Se nenhum status for encontrado
            InvalidPaginationError: Se os parâmetros de paginação forem inválidos
            InternalServerError: Para outros erros internos
        """
        pass
