"""
Composer responsável por montar a cadeia de dependências para o endpoint de deleção de fiscal.

Retorna o handler do controller, que recebe um HttpRequest e retorna um HttpResponse.

Fluxo:
- Instancia FiscalRepository com o handler de conexão
- Instancia o use case DeleteFiscal
- Instancia o controller DeleteFiscalController
- Retorna o método handle do controller
"""

from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.fiscal_repository import FiscalRepository
from src.data.use_cases.delete_fiscal import DeleteFiscal
from src.presentation.controllers.delete_fiscal_controller import DeleteFiscalController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def delete_fiscal_composer() -> Callable[[HttpRequest], HttpResponse]:
    return DeleteFiscalController(
        delete_fiscal_case=DeleteFiscal(
            fiscal_repository=FiscalRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        )
    ).handle