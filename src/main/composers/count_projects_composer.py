from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.project_repository import ProjectRepository
from src.data.use_cases.count_projects import CountProjects
from src.presentation.controllers.count_projects_controller import CountProjectsController
from typing import Callable
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

def count_projects_composer() -> Callable[[HttpRequest], HttpResponse]:
    return CountProjectsController(
        count_projects=CountProjects(
            project_repository=ProjectRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        )
    ).handle