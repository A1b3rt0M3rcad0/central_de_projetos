from src.data.use_cases.create_history_project import CreateHistoryProject
from src.presentation.controllers.create_history_project_controller import CreateHistoryProjectController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.infra.relational.repository.history_project import HistoryProjectRepository
from src.infra.relational.config.connection.db_connection_handler import DBConnectionHandler
from src.infra.relational.config.connection.string_connection import StringConnection
from typing import Callable

def create_history_project_composer() -> Callable[[HttpRequest], HttpResponse]:
    return CreateHistoryProjectController(
        CreateHistoryProject(
            HistoryProjectRepository(
                DBConnectionHandler(
                    StringConnection()
                )
            )
        )
    ).handle