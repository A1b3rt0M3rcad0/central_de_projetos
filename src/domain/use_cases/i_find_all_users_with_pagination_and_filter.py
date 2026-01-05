from abc import ABC, abstractmethod
from typing import Dict, Any

class IFindAllUsersWithPaginationAndFilter(ABC):
    """
    Interface para buscar todos os usuários com paginação e filtro global.
    """

    @abstractmethod
    def find(self, page_size: int, page: int, search_term: str = None) -> Dict[str, Any]:
        """
        Busca todos os usuários com paginação e filtro opcional.

        Args:
            page_size: Número de itens por página
            page: Número da página (baseado em 1)
            search_term: Termo de busca opcional para filtrar usuários

        Returns:
            Dict contendo:
                - users: Lista de usuários da página atual
                - total_items: Total de usuários no sistema (com filtro aplicado)
                - total_pages: Total de páginas
                - current_page: Página atual
                - page_size: Tamanho da página

        Raises:
            UsersNotFoundError: Se nenhum usuário for encontrado
            InvalidPaginationError: Se os parâmetros de paginação forem inválidos
            InternalServerError: Para outros erros internos
        """
