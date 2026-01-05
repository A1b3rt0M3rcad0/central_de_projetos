from src.domain.use_cases.i_get_projects_with_pagination_and_filter import IGetProjectsWithPaginationAndFilter
from src.data.interface.i_project_repository import IProjectRepository
from typing import Dict, Any
import math

class GetProjectsWithPaginationAndFilter(IGetProjectsWithPaginationAndFilter):
    """
    Implementação do caso de uso para buscar projetos com paginação e filtro.
    """

    def __init__(self, project_repository: IProjectRepository):
        self.__project_repository = project_repository

    def get(self, page_size: int, page: int, search_term: str = None) -> Dict[str, Any]:
        """
        Busca projetos com paginação e filtro opcional.

        Args:
            page_size: Número de itens por página
            page: Número da página (baseado em 1)
            search_term: Termo de busca opcional para filtrar projetos

        Returns:
            Dict contendo os projetos paginados e informações de paginação

        Raises:
            Exception: Para erros de repositório ou validação
        """
        try:
            # Validar parâmetros
            if page_size <= 0:
                raise ValueError("page_size deve ser maior que 0")
            if page <= 0:
                raise ValueError("page deve ser maior que 0")

            # Buscar projetos paginados com filtro
            projects = self.__project_repository.get_projects_with_pagination_and_filter(page_size, page, search_term)
            
            # Contar total de projetos com filtro
            total_items = self.__project_repository.count_projects_with_filter(search_term)
            
            # Calcular total de páginas
            total_pages = math.ceil(total_items / page_size) if total_items > 0 else 1
            
            return {
                'projects': projects,
                'total_items': total_items,
                'total_pages': total_pages,
                'current_page': page,
                'page_size': page_size
            }
            
        except Exception as e:
            raise e from e
