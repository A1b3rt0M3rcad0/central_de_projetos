from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.project_bairro_repository import ProjectBairroRepository
from src.data.use_cases.get_project_verba_by_bairro import GetProjectVerbaByBairro
from src.presentation.controllers.get_project_verba_by_bairro_controller import GetProjectVerbaByBairroController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def get_project_verba_by_bairro() -> Callable[[HttpRequest], HttpResponse]:
    return GetProjectVerbaByBairroController(
        get_project_verba_by_bairro=GetProjectVerbaByBairro(
            project_bairro_repository=ProjectBairroRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        )
    ).handle