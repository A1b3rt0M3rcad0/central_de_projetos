from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.fiscal_repository import FiscalRepository
from src.data.use_cases.update_fiscal_status import UpdateFiscalStatus
from src.presentation.controllers.update_fiscal_status_controller import UpdateFiscalStatusController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def update_fiscal_status_composer() -> Callable[[HttpRequest], HttpResponse]:
    return UpdateFiscalStatusController(
        update_fiscal_status_case=UpdateFiscalStatus(
            fiscal_repository=FiscalRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        )
    ).handle

