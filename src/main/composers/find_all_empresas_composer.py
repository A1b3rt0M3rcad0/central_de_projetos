from src.presentation.controllers.find_all_empresas_controller import FindAllEmpresasController
from src.data.use_cases.find_all_empresas import FindAllEmpresas
from src.infra.relational.repository.empresa_repository import EmpresaRepository
from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def find_empresas_composer() -> Callable[[HttpRequest], HttpResponse]:
    return FindAllEmpresasController(
        find_all_empresas_case=FindAllEmpresas(
            empresa_repository=EmpresaRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        )
    ).handle