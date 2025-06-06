from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.project_empresa_repository import ProjectEmpresaRepository
from src.infra.relational.repository.history_project_repository import HistoryProjectRepository
from src.data.use_cases.create_project_empresa import CreateProjectEmpresa
from src.data.use_cases.create_history_project import CreateHistoryProject
from src.presentation.controllers.create_project_empresa_controller import CreateProjectEmpresaController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def create_project_empresa_composer() -> Callable[[HttpRequest], HttpResponse]:
    return CreateProjectEmpresaController(
        create_project_empresa_case=CreateProjectEmpresa(
            project_empresa_repository=ProjectEmpresaRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        ),
        create_history_project_case=CreateHistoryProject(
            history_project_repository=HistoryProjectRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        )
    ).handle