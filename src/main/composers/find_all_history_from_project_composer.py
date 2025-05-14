from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.history_project import HistoryProjectRepository
from src.data.use_cases.find_all_history_from_project import FindAllHistoryFromProject
from src.presentation.controllers.find_all_history_from_project_controller import FindAllHistoryFromProjectController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def find_all_history_from_project_composer() -> Callable[[HttpRequest], HttpResponse]:
    return FindAllHistoryFromProjectController(
        find_all_history_from_project=FindAllHistoryFromProject(
            history_project_repository=HistoryProjectRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        )
    ).handle