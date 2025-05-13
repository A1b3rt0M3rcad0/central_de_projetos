from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.presentation.controllers.create_project_controller import CreateProjectController
from src.data.use_cases.create_project import CreateProject
from src.data.use_cases.create_history_project import CreateHistoryProject
from src.data.use_cases.find_project_by_name import FindProjectByName
from src.infra.relational.repository.project_repository import ProjectRepository
from src.infra.relational.repository.history_project import HistoryProjectRepository
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def create_project_composer() -> Callable[[HttpRequest], HttpResponse]:
    return CreateProjectController(
        create_history_project_case=CreateHistoryProject(HistoryProjectRepository(db_connection_handler_factory())),
        create_project_case=CreateProject(ProjectRepository(db_connection_handler_factory())),
        find_project_by_name_case=FindProjectByName(ProjectRepository(db_connection_handler_factory()))
    ).handle