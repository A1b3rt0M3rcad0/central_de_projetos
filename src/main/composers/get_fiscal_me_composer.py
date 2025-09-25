from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.presentation.controllers.get_fiscal_me_controller import GetFiscalMeController
from src.data.use_cases.find_fiscal_by_id import FindFiscalById
from src.infra.relational.repository.fiscal_repository import FiscalRepository
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable


def get_fiscal_me_composer() -> Callable[[HttpRequest], HttpResponse]:
    return GetFiscalMeController(
        find_fiscal_by_id_case=FindFiscalById(
            FiscalRepository(db_connection_handler_factory())
        )
    ).handle


