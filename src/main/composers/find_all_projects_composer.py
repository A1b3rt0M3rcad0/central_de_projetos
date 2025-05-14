from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.project_repository import ProjectRepository
from src.data.use_cases.find_all_project import FindAllProjects
from src.presentation.controllers.find_all_projects_controller import FindAllProjectsController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def find_all_projects_composer() -> Callable[[HttpRequest], HttpResponse]:
    return FindAllProjectsController(
        find_all_projects_case=FindAllProjects(
            project_repository=ProjectRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        )
    ).handle