from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.project_empresa_repository import ProjectEmpresaRepository
from src.data.use_cases.create_project_empresa import CreateProjectEmpresa
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
        )
    ).handle