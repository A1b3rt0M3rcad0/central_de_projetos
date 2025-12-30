from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.project_folder_repository import ProjectFolderRepository
from src.infra.relational.repository.folder_repository import FolderRepository
from src.data.use_cases.find_all_folders_from_project import FindAllFoldersFromProject
from src.data.use_cases.find_folder_by_id import FindFolderById
from src.presentation.controllers.find_all_folders_from_project_controller import FindAllFoldersFromProjectController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def find_all_folders_from_project_composer() -> Callable[[HttpRequest], HttpResponse]:
    return FindAllFoldersFromProjectController(
        find_all_folders_from_project_case=FindAllFoldersFromProject(
            project_folder_repository=ProjectFolderRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        ),
        find_folder_by_id=FindFolderById(
            folder_repository=FolderRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        )
    ).handle

