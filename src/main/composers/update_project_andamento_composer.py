from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.project_repository import ProjectRepository
from src.infra.relational.repository.history_project_repository import HistoryProjectRepository
from src.data.use_cases.update_project_andamento import UpdateProjectAndamento
from src.data.use_cases.create_history_project import CreateHistoryProject
from src.presentation.controllers.update_project_andamento_controller import UpdateProjectAndamentoController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def update_project_andamento_composer() -> Callable[[HttpRequest], HttpResponse]:
    return UpdateProjectAndamentoController(
        create_history_project_case=CreateHistoryProject(
            history_project_repository=HistoryProjectRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        ),
        update_project_andamento_case=UpdateProjectAndamento(
            project_repository=ProjectRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        )
    ).handle