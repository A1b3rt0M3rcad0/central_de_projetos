from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.project_bairro_repository import ProjectBairroRepository
from src.infra.relational.repository.history_project_repository import HistoryProjectRepository
from src.data.use_cases.update_bairro_from_project import UpdateBairroFromProject
from src.data.use_cases.create_history_project import CreateHistoryProject
from src.presentation.controllers.update_bairro_from_project_controller import UpdateBairroFromProjectController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def update_bairro_from_project_composer() -> Callable[[HttpRequest], HttpResponse]:
    return UpdateBairroFromProjectController(
        create_history_project_case=CreateHistoryProject(
            history_project_repository=HistoryProjectRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        ),
        update_bairro_from_project_case=UpdateBairroFromProject(
            project_bairro_repository=ProjectBairroRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        )
    ).handle