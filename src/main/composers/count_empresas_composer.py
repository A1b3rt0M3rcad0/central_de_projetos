from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.empresa_repository import EmpresaRepository
from src.data.use_cases.count_empresas import CountEmpresas
from src.presentation.controllers.count_empresas_controller import CountEmpresasController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def count_empresas_composer() -> Callable[[HttpRequest], HttpResponse]:
    return CountEmpresasController(
        count_empresas=CountEmpresas(
            empresa_repository=EmpresaRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        )
    ).handle