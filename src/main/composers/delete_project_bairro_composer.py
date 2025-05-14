from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.project_bairro_repository import ProjectBairroRepository
from src.data.use_cases.delete_project_bairro import DeleteProjectBairro
from src.presentation.controllers.delete_project_bairro_controller import DeleteProjectBairroController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def delete_project_bairro_composer() -> Callable[[HttpRequest], HttpResponse]:
    return DeleteProjectBairroController(
        delete_project_bairro_case=DeleteProjectBairro(
            project_bairro_repository=ProjectBairroRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        )
    ).handle