from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.presentation.controllers.get_latest_work_projects_by_fiscal_controller import GetLatestWorkProjectsByFiscalController
from src.data.use_cases.get_latest_work_projects_by_fiscal import GetLatestWorkProjectsByFiscal
from src.infra.relational.repository.work_project_repository import WorkProjectRepository
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def get_latest_work_projects_by_fiscal_composer() -> Callable[[HttpRequest], HttpResponse]:
    return GetLatestWorkProjectsByFiscalController(
        get_latest_work_projects_by_fiscal_case=GetLatestWorkProjectsByFiscal(WorkProjectRepository(db_connection_handler_factory()))
    ).handle 