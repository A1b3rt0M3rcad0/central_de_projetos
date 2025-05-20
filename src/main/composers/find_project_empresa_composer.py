from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.project_empresa_repository import ProjectEmpresaRepository
from src.data.use_cases.find_project_empresa import FindProjectEmpresa
from src.presentation.controllers.find_project_empresa_controller import FindProjectEmpresaController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def find_project_empresa_composer() -> Callable[[HttpRequest], HttpResponse]:
    return FindProjectEmpresaController(
        find_project_empresa_case=FindProjectEmpresa(
            project_empresa_repository=ProjectEmpresaRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        )
    ).handle