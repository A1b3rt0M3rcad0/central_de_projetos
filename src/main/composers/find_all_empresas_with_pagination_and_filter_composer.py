from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.empresa_repository import EmpresaRepository
from src.data.use_cases.find_all_empresas_with_pagination_and_filter import FindAllEmpresasWithPaginationAndFilter
from src.presentation.controllers.find_all_empresas_with_pagination_and_filter_controller import FindAllEmpresasWithPaginationAndFilterController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def find_all_empresas_with_pagination_and_filter_composer() -> Callable[[HttpRequest], HttpResponse]:
    """Composer para o caso de uso de buscar empresas com paginação e filtro."""
    
    return FindAllEmpresasWithPaginationAndFilterController(
        find_all_empresas_with_pagination_and_filter_case=FindAllEmpresasWithPaginationAndFilter(
            empresa_repository=EmpresaRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        )
    ).handle
