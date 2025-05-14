from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.user_repository import UserRepository
from src.data.use_cases.delete_user import DeleteUser
from src.presentation.controllers.delete_user_controller import DeleteUserController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def delete_user_composer() -> Callable[[HttpRequest], HttpResponse]:
    return DeleteUserController(
        delete_user_case=DeleteUser(
            user_repository=UserRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        )
    ).handle