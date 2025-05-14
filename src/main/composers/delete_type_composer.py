from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.data.use_cases.delete_type import DeleteType
from src.infra.relational.repository.types_repository import TypesRepository
from src.presentation.controllers.delete_type_controller import DeleteTypeController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def delete_type_composer() -> Callable[[HttpRequest], HttpResponse]:
    return DeleteTypeController(
        delete_type_case=DeleteType(
            types_repository=TypesRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        )
    ).handle