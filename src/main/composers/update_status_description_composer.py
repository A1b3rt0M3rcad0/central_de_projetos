from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.status_repository import StatusRepository
from src.data.use_cases.update_status_description import UpdateStatusDescription
from src.presentation.controllers.update_status_description_controller import UpdateStatusDescriptionController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def update_status_description_composer() -> Callable[[HttpRequest], HttpResponse]:
    return UpdateStatusDescriptionController(
        update_status_description_case=UpdateStatusDescription(
            status_repository=StatusRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        )
    ).handle