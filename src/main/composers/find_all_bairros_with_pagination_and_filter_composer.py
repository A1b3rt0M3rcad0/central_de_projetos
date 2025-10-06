from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.bairro_repository import BairroRepository
from src.data.use_cases.find_all_bairros_with_pagination_and_filter import FindAllBairrosWithPaginationAndFilter
from src.presentation.controllers.find_all_bairros_with_pagination_and_filter_controller import FindAllBairrosWithPaginationAndFilterController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def find_all_bairros_with_pagination_and_filter_composer() -> Callable[[HttpRequest], HttpResponse]:
    """Composer para o caso de uso de buscar bairros com paginação e filtro."""
    
    return FindAllBairrosWithPaginationAndFilterController(
        find_all_bairros_with_pagination_and_filter_case=FindAllBairrosWithPaginationAndFilter(
            bairro_repository=BairroRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        )
    ).handle
