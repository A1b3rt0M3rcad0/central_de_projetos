from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.user_repository import UserRepository
from src.data.use_cases.find_all_user_by_role import FindAllUserByRole
from src.presentation.controllers.find_all_user_by_role_controller import FindAllUserByRoleController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def find_all_user_by_role_composer() -> Callable[[HttpRequest], HttpResponse]:
    return FindAllUserByRoleController(
        find_all_user_by_role_case=FindAllUserByRole(
            user_project_repository=UserRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        )
    ).handle