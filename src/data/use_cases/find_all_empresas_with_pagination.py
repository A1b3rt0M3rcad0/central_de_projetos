from src.domain.use_cases.i_find_all_empresas_with_pagination import IFindAllEmpresasWithPagination
from src.data.interface.i_empresa_repository import IEmpresaRepository
from typing import Dict, Any
import math

class FindAllEmpresasWithPagination(IFindAllEmpresasWithPagination):
    """
    Implementação do caso de uso para buscar todas as empresas com paginação.
    """

    def __init__(self, empresa_repository: IEmpresaRepository):
        self.__empresa_repository = empresa_repository

    def find(self, page_size: int, page: int) -> Dict[str, Any]:
        """
        Busca todas as empresas com paginação.

        Args:
            page_size: Número de itens por página
            page: Número da página (baseado em 1)

        Returns:
            Dict contendo as empresas paginadas e informações de paginação

        Raises:
            Exception: Para erros de repositório ou validação
        """
        try:
            # Validar parâmetros
            if page_size <= 0:
                raise ValueError("page_size deve ser maior que 0")
            if page <= 0:
                raise ValueError("page deve ser maior que 0")

            # Buscar empresas paginadas
            empresas = self.__empresa_repository.find_all_with_pagination(page_size, page)
            
            # Contar total de empresas
            total_items = self.__empresa_repository.count_all()
            
            # Calcular total de páginas
            total_pages = math.ceil(total_items / page_size) if total_items > 0 else 1
            
            return {
                'empresas': empresas,
                'total_items': total_items,
                'total_pages': total_pages,
                'current_page': page,
                'page_size': page_size
            }
            
        except Exception as e:
            raise e from e
