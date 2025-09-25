from abc import ABC, abstractmethod
from typing import Dict, Any

class IFindAllStatusWithPagination(ABC):
    """
    Interface para buscar todos os status com paginação.
    """

    @abstractmethod
    def find(self, page_size: int, page: int) -> Dict[str, Any]:
        """
        Busca todos os status com paginação.

        Args:
            page_size: Número de itens por página
            page: Número da página (baseado em 1)

        Returns:
            Dict contendo:
                - status: Lista de status da página atual
                - total_items: Total de status no sistema
                - total_pages: Total de páginas
                - current_page: Página atual
                - page_size: Tamanho da página

        Raises:
            StatusNotFoundError: Se nenhum status for encontrado
            InternalServerError: Para outros erros durante a operação
        """
