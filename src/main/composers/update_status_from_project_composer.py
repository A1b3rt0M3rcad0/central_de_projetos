from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.project_repository import ProjectRepository
from src.data.use_cases.update_status_from_project import UpdateStatusFromProject
from src.presentation.controllers.update_status_from_project_controller import UpdateStatusFromProjectController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def update_status_from_project_composer() -> Callable[[HttpRequest], HttpResponse]:
    return UpdateStatusFromProjectController(
        update_status_from_project=UpdateStatusFromProject(
            project_repository=ProjectRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        )
    ).handle