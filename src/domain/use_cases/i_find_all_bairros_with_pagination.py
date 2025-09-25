from abc import ABC, abstractmethod
from typing import Dict, Any

class IFindAllBairrosWithPagination(ABC):
    """
    Interface para buscar todos os bairros com paginação.
    """

    @abstractmethod
    def find(self, page_size: int, page: int) -> Dict[str, Any]:
        """
        Busca todos os bairros com paginação.

        Args:
            page_size: Número de itens por página
            page: Número da página (baseado em 1)

        Returns:
            Dict contendo:
                - bairros: Lista de bairros da página atual
                - total_items: Total de bairros no sistema
                - total_pages: Total de páginas
                - current_page: Página atual
                - page_size: Tamanho da página

        Raises:
            BairrosNotFoundError: Se nenhum bairro for encontrado
            InvalidPaginationError: Se os parâmetros de paginação forem inválidos
            InternalServerError: Para outros erros internos
        """
        pass
