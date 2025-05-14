from src.data.use_cases.create_type import CreateType
from src.infra.relational.repository.types_repository import TypesRepository
from src.presentation.controllers.create_type_controller import CreateTypeController
from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def create_type_composer() -> Callable[[HttpRequest], HttpResponse]:
    return CreateTypeController(
        create_type_case=CreateType(
            types_repository=TypesRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        )
    ).handle