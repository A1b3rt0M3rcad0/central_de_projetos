from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.types_repository import TypesRepository
from src.data.use_cases.find_all_types_with_pagination_and_filter import FindAllTypesWithPaginationAndFilter
from src.presentation.controllers.find_all_types_with_pagination_and_filter_controller import FindAllTypesWithPaginationAndFilterController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def find_all_types_with_pagination_and_filter_composer() -> Callable[[HttpRequest], HttpResponse]:
    """Composer para o caso de uso de buscar tipos com paginação e filtro."""
    
    return FindAllTypesWithPaginationAndFilterController(
        find_all_types_with_pagination_and_filter_case=FindAllTypesWithPaginationAndFilter(
            types_repository=TypesRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        )
    ).handle
