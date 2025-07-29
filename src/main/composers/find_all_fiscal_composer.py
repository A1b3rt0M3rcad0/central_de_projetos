"""
Composer responsável por montar a cadeia de dependências para o endpoint de busca de todos os fiscais.

Retorna o handler do controller, que recebe um HttpRequest e retorna um HttpResponse.

Fluxo:
- Instancia FiscalRepository com o handler de conexão
- Instancia o use case FindAllFiscal
- Instancia o controller FindAllFiscalController
- Retorna o método handle do controller
"""

from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.fiscal_repository import FiscalRepository
from src.data.use_cases.find_all_fiscal import FindAllFiscal
from src.presentation.controllers.find_all_fiscal_controller import FindAllFiscalController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def find_all_fiscal_composer() -> Callable[[HttpRequest], HttpResponse]:
    return FindAllFiscalController(
        find_all_fiscal_case=FindAllFiscal(
            fiscal_repository=FiscalRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        )
    ).handle