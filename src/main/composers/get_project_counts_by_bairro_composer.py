from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.project_bairro_repository import ProjectBairroRepository
from src.data.use_cases.get_project_counts_by_bairro import GetProjectCountsByBairro
from src.presentation.controllers.get_project_counts_by_bairro_controller import GetProjectCountsByBairroController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def get_project_counts_by_bairro_composer() -> Callable[[HttpRequest], HttpResponse]:
    return GetProjectCountsByBairroController(
        get_project_counts_by_bairro=GetProjectCountsByBairro(
            project_bairro_repository=ProjectBairroRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        )
    ).handle