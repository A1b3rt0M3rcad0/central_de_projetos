from src.presentation.controllers.create_fiscal_controller import CreateFiscalController
from src.data.use_cases.create_fiscal import CreateFiscal
from src.infra.relational.repository.fiscal_repository import FiscalRepository
from src.infra.relational.config.connection.db_connection_handler import DBConnectionHandler
from src.infra.relational.config.connection.string_connection import StringConnection
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def create_fiscal_composer() -> Callable[[HttpRequest], HttpResponse]:
    return CreateFiscalController(
        CreateFiscal(
            FiscalRepository(
                DBConnectionHandler(
                    StringConnection()
                )
            )
        )
    )