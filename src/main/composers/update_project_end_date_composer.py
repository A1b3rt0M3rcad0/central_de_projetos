from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.project_repository import ProjectRepository
from src.infra.relational.repository.history_project import HistoryProjectRepository
from src.data.use_cases.update_project_end_date import UpdateProjectEndDate
from src.data.use_cases.create_history_project import CreateHistoryProject
from src.presentation.controllers.update_project_end_date_controller import UpdateProjectEndDateController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def update_project_end_date_composer() -> Callable[[HttpRequest], HttpResponse]:
    return UpdateProjectEndDateController(
        create_history_project_case=CreateHistoryProject(
            history_project_repository=HistoryProjectRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        ),
        update_project_end_date_case=UpdateProjectEndDate(
            project_repository=ProjectRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        )
    ).handle