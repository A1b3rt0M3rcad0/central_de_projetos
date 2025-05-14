from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.user_repository import UserRepository
from src.data.use_cases.update_user_password import UpdateUserPassword
from src.presentation.controllers.update_user_password_controller import UpdateUserPasswordController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def update_user_password_composer() -> Callable[[HttpRequest], HttpResponse]:
    return UpdateUserPasswordController(
        update_user_password_case=UpdateUserPassword(
            user_repository=UserRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        )
    ).handle