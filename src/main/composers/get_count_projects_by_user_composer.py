from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.user_repository import UserRepository
from src.data.use_cases.get_count_projects_by_user import GetCountProjectsByUser
from src.presentation.controllers.get_count_projects_by_user_controller import GetCountProjectsByUserController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def get_count_projets_by_user_composer() -> Callable[[HttpRequest], HttpResponse]:
    return GetCountProjectsByUserController(
        get_count_projects_by_user=GetCountProjectsByUser(
            user_repository=UserRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        )
    ).handle