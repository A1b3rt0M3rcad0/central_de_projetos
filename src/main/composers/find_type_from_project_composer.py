from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.project_type_repository import ProjectTypeRepository
from src.data.use_cases.find_type_from_project import FindTypeFromProject
from src.presentation.controllers.find_type_from_project_controller import FindTypeFromProjectController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def find_type_from_project_composer() -> Callable[[HttpRequest], HttpResponse]:
    return FindTypeFromProjectController(
        find_type_from_project_case=FindTypeFromProject(
            project_type_repository=ProjectTypeRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        )
    ).handle