from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.types_repository import TypesRepository
from src.data.use_cases.update_type import UpdateType
from src.presentation.controllers.update_type_controller import UpdateTypeController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def update_type_composer() -> Callable[[HttpRequest], HttpResponse]:
    return UpdateTypeController(
        update_type_case=UpdateType(
            types_repository=TypesRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        )
    ).handle