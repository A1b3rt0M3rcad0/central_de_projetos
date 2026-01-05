from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.project_repository import ProjectRepository
from src.data.use_cases.get_projects_with_pagination_and_filter import GetProjectsWithPaginationAndFilter
from src.presentation.controllers.get_projects_with_pagination_and_filter_controller import GetProjectsWithPaginationAndFilterController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def get_projects_with_pagination_and_filter_composer() -> Callable[[HttpRequest], HttpResponse]:
    """Composer para o caso de uso de buscar projetos com paginação e filtro."""
    
    return GetProjectsWithPaginationAndFilterController(
        get_projects_with_pagination_and_filter_case=GetProjectsWithPaginationAndFilter(
            project_repository=ProjectRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        )
    ).handle
