from src.data.use_cases.create_empresa import CreateEmpresa
from src.infra.relational.repository.empresa_repository import EmpresaRepository
from src.infra.relational.config.connection.db_connection_handler import DBConnectionHandler
from src.infra.relational.config.connection.string_connection import StringConnection
from src.presentation.controllers.create_empresa_controller import CreateEmpresaController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def create_empresa_composer() -> Callable[[HttpRequest], HttpResponse]:
    return CreateEmpresaController(
        CreateEmpresa(
            EmpresaRepository(
                DBConnectionHandler(
                    StringConnection()
                )
            )
        )
    ).handle