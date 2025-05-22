from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.types_repository import TypesRepository
from src.data.use_cases.find_all_types import FindAllTypes
from src.presentation.controllers.find_all_types_controller import FindAllTypesController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def find_all_types_composer() -> Callable[[HttpRequest], HttpResponse]:
    return FindAllTypesController(
        find_all_types_case=FindAllTypes(
            types_repository=TypesRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        )
    ).handle