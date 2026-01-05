from abc import ABC, abstractmethod
from typing import Dict, Any

class IFindAllEmpresasWithPagination(ABC):
    """
    Interface para buscar todas as empresas com paginação.
    """

    @abstractmethod
    def find(self, page_size: int, page: int) -> Dict[str, Any]:
        """
        Busca todas as empresas com paginação.

        Args:
            page_size: Número de itens por página
            page: Número da página (baseado em 1)

        Returns:
            Dict contendo:
                - empresas: Lista de empresas da página atual
                - total_items: Total de empresas no sistema
                - total_pages: Total de páginas
                - current_page: Página atual
                - page_size: Tamanho da página

        Raises:
            EmpresasNotFoundError: Se nenhuma empresa for encontrada
            InvalidPaginationError: Se os parâmetros de paginação forem inválidos
            InternalServerError: Para outros erros internos
        """
        pass
