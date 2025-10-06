from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.status_repository import StatusRepository
from src.data.use_cases.find_all_status_with_pagination_and_filter import FindAllStatusWithPaginationAndFilter
from src.presentation.controllers.find_all_status_with_pagination_and_filter_controller import FindAllStatusWithPaginationAndFilterController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def find_all_status_with_pagination_and_filter_composer() -> Callable[[HttpRequest], HttpResponse]:
    """Composer para o caso de uso de buscar status com paginação e filtro."""
    
    return FindAllStatusWithPaginationAndFilterController(
        find_all_status_with_pagination_and_filter_case=FindAllStatusWithPaginationAndFilter(
            status_repository=StatusRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        )
    ).handle
