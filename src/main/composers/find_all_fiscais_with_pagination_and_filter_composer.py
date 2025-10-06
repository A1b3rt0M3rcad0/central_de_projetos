from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.fiscal_repository import FiscalRepository
from src.data.use_cases.find_all_fiscais_with_pagination_and_filter import FindAllFiscaisWithPaginationAndFilter
from src.presentation.controllers.find_all_fiscais_with_pagination_and_filter_controller import FindAllFiscaisWithPaginationAndFilterController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def find_all_fiscais_with_pagination_and_filter_composer() -> Callable[[HttpRequest], HttpResponse]:
    """Composer para o caso de uso de buscar fiscais com paginação e filtro."""
    
    return FindAllFiscaisWithPaginationAndFilterController(
        find_all_fiscais_with_pagination_and_filter_case=FindAllFiscaisWithPaginationAndFilter(
            fiscal_repository=FiscalRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        )
    ).handle
