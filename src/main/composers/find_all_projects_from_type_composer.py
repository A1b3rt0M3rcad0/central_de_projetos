from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.project_type_repository import ProjectTypeRepository
from src.infra.relational.repository.project_repository import ProjectRepository
from src.data.use_cases.find_all_projects_from_type import FindAllProjectsFromType
from src.data.use_cases.find_project import FindProject
from src.presentation.controllers.find_all_projects_from_type_controller import FindAllProjectsFromTypeController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def find_all_projects_from_type_composer() -> Callable[[HttpRequest], HttpResponse]:
    db_handler = db_connection_handler_factory()
    return FindAllProjectsFromTypeController(
        find_all_projects_from_type_case=FindAllProjectsFromType(
            project_type_repository=ProjectTypeRepository(
                db_connection_handler=db_handler
            )
        ),
        find_project_case=FindProject(
            project_repository=ProjectRepository(
                db_connection_handler=db_handler
            )
        )
    ).handle

