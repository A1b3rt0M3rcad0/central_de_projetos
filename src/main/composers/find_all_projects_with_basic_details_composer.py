from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.project_repository import ProjectRepository
from src.infra.relational.repository.user_project_repository import UserProjectRepository
from src.data.use_cases.find_all_projects_with_basic_details import FindAllProjectsWithBasicDetails
from src.presentation.controllers.find_all_projects_with_basic_details_controller import FindAllProjectsWithBasicDetailsController
from src.data.use_cases.find_user_by_project_id import FindUserByProjectId
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def find_all_projects_with_basic_details_composer() -> Callable[[HttpRequest], HttpResponse]:
    return FindAllProjectsWithBasicDetailsController(
        find_all_projects_with_basic_details_case=FindAllProjectsWithBasicDetails(
            project_repository=ProjectRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        ),
        find_user_by_project_id_case=FindUserByProjectId(
            user_project_repository=UserProjectRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        )
    ).handle