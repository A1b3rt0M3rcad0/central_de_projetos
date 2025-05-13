from src.data.use_cases.create_status import CreateStatus
from src.presentation.controllers.create_status_controller import CreateStatusController
from src.infra.relational.repository.status_repository import StatusRepository
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from typing import Callable

def create_status_composer() -> Callable[[HttpRequest], HttpResponse]:
    return CreateStatusController(
        create_status_case=CreateStatus(
            status_repository=StatusRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        )
    ).handle