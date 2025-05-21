from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.project_type_repository import ProjectTypeRepository
from src.data.use_cases.create_project_type import CreateProjectType
from src.presentation.controllers.create_project_type_controller import CreateProjectTypeController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def create_project_type_composer() -> Callable[[HttpRequest], HttpResponse]:
    return CreateProjectTypeController(
        create_project_type_case=CreateProjectType(
            project_type_repository=ProjectTypeRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        )
    ).handle