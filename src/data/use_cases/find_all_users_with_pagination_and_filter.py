from src.domain.use_cases.i_find_all_users_with_pagination_and_filter import IFindAllUsersWithPaginationAndFilter
from src.data.interface.i_user_repository import IUserRepository
from typing import Dict, Any
import math

class FindAllUsersWithPaginationAndFilter(IFindAllUsersWithPaginationAndFilter):
    """
    Implementação do caso de uso para buscar todos os usuários com paginação e filtro.
    """

    def __init__(self, user_repository: IUserRepository):
        self.__user_repository = user_repository

    def find(self, page_size: int, page: int, search_term: str = None) -> Dict[str, Any]:
        """
        Busca todos os usuários com paginação e filtro opcional.

        Args:
            page_size: Número de itens por página
            page: Número da página (baseado em 1)
            search_term: Termo de busca opcional para filtrar usuários

        Returns:
            Dict contendo os usuários paginados e informações de paginação

        Raises:
            Exception: Para erros de repositório ou validação
        """
        try:
            # Validar parâmetros
            if page_size <= 0:
                raise ValueError("page_size deve ser maior que 0")
            if page <= 0:
                raise ValueError("page deve ser maior que 0")

            # Buscar usuários paginados com filtro
            users = self.__user_repository.find_all_with_pagination_and_filter(page_size, page, search_term)
            
            # Contar total de usuários com filtro
            total_items = self.__user_repository.count_all_with_filter(search_term)
            
            # Calcular total de páginas
            total_pages = math.ceil(total_items / page_size) if total_items > 0 else 1
            
            return {
                'users': users,
                'total_items': total_items,
                'total_pages': total_pages,
                'current_page': page,
                'page_size': page_size
            }
            
        except Exception as e:
            raise e from e
