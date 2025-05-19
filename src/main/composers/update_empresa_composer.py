from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.empresa_repository import EmpresaRepository
from src.data.use_cases.update_empresa import UpdateEmpresa
from src.presentation.controllers.update_empresa_controller import UpdateEmpresaController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def update_empresas_composer() -> Callable[[HttpResponse], HttpRequest]:
    return UpdateEmpresaController(
        update_empresa_case=UpdateEmpresa(
            empresa_repository=EmpresaRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        )
    ).handle