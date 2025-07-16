from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.project_repository import ProjectRepository
from src.data.use_cases.get_projects_with_pagination import GetProjectsWithPagination
from src.presentation.controllers.get_projects_with_pagination_controller import GetProjectsWithPaginationController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def get_projects_with_pagination_composer() -> Callable[[HttpRequest], HttpResponse]:
    return GetProjectsWithPaginationController(
        get_projects_with_pagination=GetProjectsWithPagination(
            project_repository=ProjectRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        )
    ).handle