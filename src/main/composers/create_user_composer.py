from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.user_repository import UserRepository
from src.data.use_cases.create_user import CreateUser
from src.presentation.controllers.create_user_controller import CreateUserController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def create_user_composer() -> Callable[[HttpRequest], HttpResponse]:
    return CreateUserController(
        create_user_case=CreateUser(
            user_repository=UserRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        )
    ).handle