from src.presentation.controllers.create_project_folder_controller import CreateProjectFolderController
from src.data.use_cases.create_project_folder import CreateProjectFolder
from src.data.use_cases.create_history_project import CreateHistoryProject
from src.data.use_cases.find_folder_by_id import FindFolderById
from src.infra.relational.repository.project_folder_repository import ProjectFolderRepository
from src.infra.relational.repository.history_project_repository import HistoryProjectRepository
from src.infra.relational.repository.folder_repository import FolderRepository
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from typing import Callable

def create_project_folder_composer() -> Callable[[HttpRequest], HttpResponse]:
    return CreateProjectFolderController(
        create_history_project_case=CreateHistoryProject(
            history_project_repository=HistoryProjectRepository(db_connection_handler_factory())
        ),
        create_project_folder_case=CreateProjectFolder(
            project_folder_repository=ProjectFolderRepository(db_connection_handler_factory())
        ),
        find_folder_by_id=FindFolderById(
            folder_repository=FolderRepository(db_connection_handler_factory())
        )
    ).handle

