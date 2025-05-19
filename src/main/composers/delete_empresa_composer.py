from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.empresa_repository import EmpresaRepository
from src.data.use_cases.delete_empresa import DeleteEmpresa
from src.presentation.controllers.delete_empresa_controller import DeleteEmpresaController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def delete_empresa_composer() -> Callable[[HttpRequest], HttpResponse]:
    return DeleteEmpresaController(
        delete_empresa_case=DeleteEmpresa(
            empresa_repository=EmpresaRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        )
    ).handle