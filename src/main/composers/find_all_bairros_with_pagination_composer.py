from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.bairro_repository import BairroRepository
from src.data.use_cases.find_all_bairros_with_pagination import FindAllBairrosWithPagination
from src.presentation.controllers.find_all_bairros_with_pagination_controller import FindAllBairrosWithPaginationController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def find_all_bairros_with_pagination_composer() -> Callable[[HttpRequest], HttpResponse]:
    return FindAllBairrosWithPaginationController(
        find_all_bairros_with_pagination_case=FindAllBairrosWithPagination(
            bairro_repository=BairroRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        )
    ).handle
