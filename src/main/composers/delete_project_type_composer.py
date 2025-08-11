from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.project_type_repository import ProjectTypeRepository
from src.infra.relational.repository.history_project_repository import HistoryProjectRepository
from src.data.use_cases.delete_project_type import DeleteProjectType
from src.data.use_cases.create_history_project import CreateHistoryProject
from src.presentation.controllers.delete_project_type_controller import DeleteProjectTypeController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def delete_project_type_composer() -> Callable[[HttpRequest], HttpResponse]:
    return DeleteProjectTypeController(
        delete_project_type_case=DeleteProjectType(
            project_type_repository=ProjectTypeRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        ),
        create_history_project_case=CreateHistoryProject(
            history_project_repository=HistoryProjectRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        )
    ).handle