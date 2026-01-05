from abc import ABC, abstractmethod
from typing import Dict, Any

class IFindAllFiscaisWithPagination(ABC):
    """
    Interface para buscar todos os fiscais com paginação.
    """

    @abstractmethod
    def find(self, page_size: int, page: int) -> Dict[str, Any]:
        """
        Busca todos os fiscais com paginação.

        Args:
            page_size: Número de itens por página
            page: Número da página (baseado em 1)

        Returns:
            Dict contendo:
                - fiscais: Lista de fiscais da página atual
                - total_items: Total de fiscais no sistema
                - total_pages: Total de páginas
                - current_page: Página atual
                - page_size: Tamanho da página

        Raises:
            FiscaisNotFoundError: Se nenhum fiscal for encontrado
            InvalidPaginationError: Se os parâmetros de paginação forem inválidos
            InternalServerError: Para outros erros internos
        """
        pass
