from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.fiscal_repository import FiscalRepository
from src.infra.relational.repository.project_fiscal_repository import ProjectFiscalRepository
from src.infra.relational.repository.work_project_repository import WorkProjectRepository
from src.data.use_cases.get_fiscal_summary import GetFiscalSummary
from src.presentation.controllers.get_fiscal_summary_controller import GetFiscalSummaryController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def get_fiscal_summary_composer() -> Callable[[HttpRequest], HttpResponse]:
    return GetFiscalSummaryController(
        get_fiscal_summary=GetFiscalSummary(
            fiscal_repository=FiscalRepository(
                db_connection_handler=db_connection_handler_factory()
            ),
            project_fiscal_repository=ProjectFiscalRepository(
                db_connection_handler=db_connection_handler_factory()
            ),
            work_project_repository=WorkProjectRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        )
    ).handle 