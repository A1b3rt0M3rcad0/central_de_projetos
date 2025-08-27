from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.presentation.controllers.get_latest_work_project_by_project_controller import GetLatestWorkProjectByProjectController
from src.data.use_cases.get_latest_work_project_by_project import GetLatestWorkProjectByProject
from src.infra.relational.repository.work_project_repository import WorkProjectRepository
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def get_latest_work_project_by_project_composer() -> Callable[[HttpRequest], HttpResponse]:
    return GetLatestWorkProjectByProjectController(
        get_latest_work_project_by_project_case=GetLatestWorkProjectByProject(
            work_project_repository=WorkProjectRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        )
    ).handle 