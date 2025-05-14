from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.status_repository import StatusRepository
from src.data.use_cases.find_all_status import FindAllStatus
from src.presentation.controllers.find_all_status_controller import FindAllStatusController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def find_all_status_composer() -> Callable[[HttpRequest], HttpResponse]:
    return FindAllStatusController(
        find_all_status_case=FindAllStatus(
            status_repository=StatusRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        )
    ).handle