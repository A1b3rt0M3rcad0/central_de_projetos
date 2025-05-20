from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.project_repository import ProjectRepository
from src.infra.relational.repository.history_project_repository import HistoryProjectRepository
from src.data.use_cases.create_history_project import CreateHistoryProject
from src.data.use_cases.update_project_verba import UpdateProjectVerba
from src.presentation.controllers.update_project_verba_controller import UpdateProjectVerbaController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def update_project_verba_composer() -> Callable[[HttpRequest], HttpResponse]:
    return UpdateProjectVerbaController(
        create_history_project_case=CreateHistoryProject(
            history_project_repository=HistoryProjectRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        ),
        update_project_verba_case=UpdateProjectVerba(
            project_repository=ProjectRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        )
    ).handle