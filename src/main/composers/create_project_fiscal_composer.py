from src.data.use_cases.create_project_fiscal import CreateProjectFiscal
from src.data.use_cases.create_history_project import CreateHistoryProject
from src.data.use_cases.find_fiscal_by_id import FindFiscalById
from src.presentation.controllers.create_project_fiscal_controller import CreateProjectFiscalController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.project_fiscal_repository import ProjectFiscalRepository
from src.infra.relational.repository.history_project_repository import HistoryProjectRepository
from src.infra.relational.repository.fiscal_repository import FiscalRepository
from typing import Callable

def create_project_fiscal_composer() -> Callable[[HttpRequest], HttpResponse]:
    return CreateProjectFiscalController(
        create_history_project_case=CreateHistoryProject(
            history_project_repository=HistoryProjectRepository(db_connection_handler_factory())
        ),
        create_project_fiscal_case=CreateProjectFiscal(
            project_fiscal_repository=ProjectFiscalRepository(db_connection_handler_factory())
        ),
        find_fiscal_by_id_case=FindFiscalById(
            fiscal_repository=FiscalRepository(db_connection_handler_factory())
        ),
    ).handle