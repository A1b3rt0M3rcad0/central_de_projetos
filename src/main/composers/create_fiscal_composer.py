"""
Composer responsável por montar a cadeia de dependências para o endpoint de criação de fiscal.

Retorna o handler do controller, que recebe um HttpRequest e retorna um HttpResponse.

Fluxo:
- Instancia FiscalRepository com o handler de conexão
- Instancia o use case CreateFiscal
- Instancia o controller CreateFiscalController
- Retorna o método handle do controller
"""

from src.presentation.controllers.create_fiscal_controller import CreateFiscalController
from src.data.use_cases.create_fiscal import CreateFiscal
from src.infra.relational.repository.fiscal_repository import FiscalRepository
from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def create_fiscal_composer() -> Callable[[HttpRequest], HttpResponse]:
    return CreateFiscalController(
        CreateFiscal(
            FiscalRepository(
                db_connection_handler_factory()
            )
        )
    ).handle