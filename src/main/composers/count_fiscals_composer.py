"""
Composer responsável por montar a cadeia de dependências para o endpoint de contagem de fiscais.

Retorna o handler do controller, que recebe um HttpRequest e retorna um HttpResponse.

Fluxo:
- Instancia FiscalRepository com o handler de conexão
- Instancia o use case CountFiscals
- Instancia o controller CountFiscalsController
- Retorna o método handle do controller
"""

from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.fiscal_repository import FiscalRepository
from src.data.use_cases.count_fiscals import CountFiscals
from src.presentation.controllers.count_fiscals_controller import CountFiscalsController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def count_fiscals_composer() -> Callable[[HttpRequest], HttpResponse]:
    return CountFiscalsController(
        count_fiscals=CountFiscals(
            fiscal_repository=FiscalRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        )
    ).handle