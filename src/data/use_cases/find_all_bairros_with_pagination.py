from src.domain.use_cases.i_find_all_bairros_with_pagination import IFindAllBairrosWithPagination
from src.data.interface.i_bairro_repository import IBairroRepository
from typing import Dict, Any
import math

class FindAllBairrosWithPagination(IFindAllBairrosWithPagination):
    """
    Implementação do caso de uso para buscar todos os bairros com paginação.
    """

    def __init__(self, bairro_repository: IBairroRepository):
        self.__bairro_repository = bairro_repository

    def find(self, page_size: int, page: int) -> Dict[str, Any]:
        """
        Busca todos os bairros com paginação.

        Args:
            page_size: Número de itens por página
            page: Número da página (baseado em 1)

        Returns:
            Dict contendo os bairros paginados e informações de paginação

        Raises:
            Exception: Para erros de repositório ou validação
        """
        try:
            # Validar parâmetros
            if page_size <= 0:
                raise ValueError("page_size deve ser maior que 0")
            if page <= 0:
                raise ValueError("page deve ser maior que 0")

            # Buscar bairros paginados
            bairros = self.__bairro_repository.find_all_with_pagination(page_size, page)
            
            # Contar total de bairros
            total_items = self.__bairro_repository.count_all()
            
            # Calcular total de páginas
            total_pages = math.ceil(total_items / page_size) if total_items > 0 else 1
            
            return {
                'bairros': bairros,
                'total_items': total_items,
                'total_pages': total_pages,
                'current_page': page,
                'page_size': page_size
            }
            
        except Exception as e:
            raise e from e
