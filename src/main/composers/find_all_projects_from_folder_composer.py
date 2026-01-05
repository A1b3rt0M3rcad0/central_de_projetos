from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.project_folder_repository import ProjectFolderRepository
from src.infra.relational.repository.project_repository import ProjectRepository
from src.data.use_cases.find_all_projects_from_folder import FindAllProjectsFromFolder
from src.data.use_cases.find_project import FindProject
from src.presentation.controllers.find_all_projects_from_folder_controller import FindAllProjectsFromFolderController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def find_all_projects_from_folder_composer() -> Callable[[HttpRequest], HttpResponse]:
    return FindAllProjectsFromFolderController(
        find_all_projects_from_folder_case=FindAllProjectsFromFolder(
            project_folder_repository=ProjectFolderRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        ),
        find_project_case=FindProject(
            project_repository=ProjectRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        )
    ).handle

