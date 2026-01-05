from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.fiscal_repository import FiscalRepository
from src.data.use_cases.find_all_fiscais_with_pagination import FindAllFiscaisWithPagination
from src.presentation.controllers.find_all_fiscais_with_pagination_controller import FindAllFiscaisWithPaginationController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def find_all_fiscais_with_pagination_composer() -> Callable[[HttpRequest], HttpResponse]:
    return FindAllFiscaisWithPaginationController(
        find_all_fiscais_with_pagination_case=FindAllFiscaisWithPagination(
            fiscal_repository=FiscalRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        )
    ).handle
