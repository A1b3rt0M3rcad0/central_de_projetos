from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.user_project_repository import UserProjectRepository
from src.infra.relational.repository.project_repository import ProjectRepository
from src.infra.relational.repository.user_repository import UserRepository
from src.data.use_cases.associate_vereador_with_a_project import AssociateVereadorWithAProject
from src.presentation.controllers.associate_vereador_with_a_project import AssociateVereadorWithAProjectController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def associate_vereador_with_a_project_composer() -> Callable[[HttpRequest], HttpResponse]:
    return AssociateVereadorWithAProjectController(
        associate_vereador_with_a_project_case=AssociateVereadorWithAProject(
            user_project_repository=UserProjectRepository(
                db_connection_handler=db_connection_handler_factory()
            ),
            project_repository=ProjectRepository(
                db_connection_handler=db_connection_handler_factory()
            ),
            user_repository=UserRepository(
                db_connection_handler=db_connection_handler_factory()
            ),
        )
    ).handle