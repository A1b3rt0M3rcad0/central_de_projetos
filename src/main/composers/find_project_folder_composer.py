from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.project_folder_repository import ProjectFolderRepository
from src.data.use_cases.find_project_folder import FindProjectFolder
from src.presentation.controllers.find_project_folder_controller import FindProjectFolderController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def find_project_folder_composer() -> Callable[[HttpRequest], HttpResponse]:
    return FindProjectFolderController(
        find_project_folder_case=FindProjectFolder(
            project_folder_repository=ProjectFolderRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        )
    ).handle

