from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.project_repository import ProjectRepository
from src.data.use_cases.find_all_from_project import FindAllFromProject
from src.presentation.controllers.find_all_from_project_controller import FindAllFromProjectController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def find_all_from_project_composer() -> Callable[[HttpRequest], HttpResponse]:
    return FindAllFromProjectController(
        find_all_from_project_case=FindAllFromProject(
            project_repository=ProjectRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        )
    ).handle