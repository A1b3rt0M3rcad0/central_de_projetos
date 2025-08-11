from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.presentation.controllers.get_work_projects_with_pagination_controller import GetWorkProjectsByProjectWithPaginationController
from src.data.use_cases.get_work_projects_by_project_with_pagination import GetWorkProjectsByProjectWithPagination
from src.infra.relational.repository.work_project_repository import WorkProjectRepository
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def get_work_projects_by_project_with_pagination_composer() -> Callable[[HttpRequest], HttpResponse]:
    return GetWorkProjectsByProjectWithPaginationController(
        get_work_projects_by_project_with_pagination_case=GetWorkProjectsByProjectWithPagination(WorkProjectRepository(db_connection_handler_factory()))
    ).handle 