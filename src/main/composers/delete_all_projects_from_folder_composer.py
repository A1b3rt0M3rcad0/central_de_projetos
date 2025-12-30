from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.project_folder_repository import ProjectFolderRepository
from src.data.use_cases.delete_all_projects_from_folder import DeleteAllProjectsFromFolder
from src.presentation.controllers.delete_all_projects_from_folder_controller import DeleteAllProjectsFromFolderController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def delete_all_projects_from_folder_composer() -> Callable[[HttpRequest], HttpResponse]:
    return DeleteAllProjectsFromFolderController(
        delete_all_projects_from_folder_case=DeleteAllProjectsFromFolder(
            project_folder_repository=ProjectFolderRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        )
    ).handle

