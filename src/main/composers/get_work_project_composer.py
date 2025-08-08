from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.presentation.controllers.get_work_project_controller import GetWorkProjectController
from src.data.use_cases.get_work_project import GetWorkProject
from src.infra.relational.repository.work_project_repository import WorkProjectRepository
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def get_work_project_composer() -> Callable[[HttpRequest], HttpResponse]:
    return GetWorkProjectController(
        get_work_project_case=GetWorkProject(WorkProjectRepository(db_connection_handler_factory()))
    ).handle 