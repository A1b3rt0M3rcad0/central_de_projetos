from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.user_project_repository import UserProjectRepository
from src.data.use_cases.find_all_association_from_projects import FindAllAssociationFromProject
from src.presentation.controllers.find_all_association_from_projects_controller import FindAllAssociationFromProjectsController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def find_all_association_from_projects_composer() -> Callable[[HttpRequest], HttpResponse]:
    return FindAllAssociationFromProjectsController(
        find_all_association_from_projects_case=FindAllAssociationFromProject(
            user_project_repository=UserProjectRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        )
    ).handle