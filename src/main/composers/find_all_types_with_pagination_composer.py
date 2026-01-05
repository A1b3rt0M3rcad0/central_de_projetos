from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.types_repository import TypesRepository
from src.data.use_cases.find_all_types_with_pagination import FindAllTypesWithPagination
from src.presentation.controllers.find_all_types_with_pagination_controller import FindAllTypesWithPaginationController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def find_all_types_with_pagination_composer() -> Callable[[HttpRequest], HttpResponse]:
    return FindAllTypesWithPaginationController(
        find_all_types_with_pagination_case=FindAllTypesWithPagination(
            types_repository=TypesRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        )
    ).handle
