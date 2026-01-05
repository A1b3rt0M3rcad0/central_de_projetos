from abc import ABC, abstractmethod
from typing import Dict, Any

class IFindAllTypesWithPagination(ABC):
    """
    Interface para buscar todos os tipos com paginação.
    """

    @abstractmethod
    def find(self, page_size: int, page: int) -> Dict[str, Any]:
        """
        Busca todos os tipos com paginação.

        Args:
            page_size: Número de itens por página
            page: Número da página (baseado em 1)

        Returns:
            Dict contendo:
                - types: Lista de tipos da página atual
                - total_items: Total de tipos no sistema
                - total_pages: Total de páginas
                - current_page: Página atual
                - page_size: Tamanho da página

        Raises:
            TypesNotFoundError: Se nenhum tipo for encontrado
            InvalidPaginationError: Se os parâmetros de paginação forem inválidos
            InternalServerError: Para outros erros internos
        """
        pass
