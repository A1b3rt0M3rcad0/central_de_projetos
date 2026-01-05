from src.domain.use_cases.i_find_all_status_with_pagination import IFindAllStatusWithPagination
from src.data.interface.i_status_repository import IStatusRepository
from typing import Dict, Any

class FindAllStatusWithPagination(IFindAllStatusWithPagination):
    """
    Implementação do caso de uso para buscar todos os status com paginação.
    """

    def __init__(self, status_repository: IStatusRepository):
        self.__status_repository = status_repository

    def find(self, page_size: int, page: int) -> Dict[str, Any]:
        """
        Busca todos os status com paginação.

        Args:
            page_size: Número de itens por página
            page: Número da página (baseado em 1)

        Returns:
            Dict contendo os status paginados e informações de paginação

        Raises:
            Exception: Para erros durante a operação
        """
        try:
            # Calcular offset
            offset = (page - 1) * page_size
            
            # Buscar status paginados
            status_list = self.__status_repository.find_all_with_pagination(page_size=page_size, offset=offset)
            
            # Contar total de status
            total_items = self.__status_repository.count_all()
            
            # Calcular total de páginas
            total_pages = (total_items + page_size - 1) // page_size  # Arredondamento para cima
            
            return {
                "status": status_list,
                "total_items": total_items,
                "total_pages": total_pages,
                "current_page": page,
                "page_size": page_size
            }
            
        except Exception as e:
            raise e from e
