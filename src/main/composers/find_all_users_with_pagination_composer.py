from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.user_repository import UserRepository
from src.data.use_cases.find_all_users_with_pagination import FindAllUsersWithPagination
from src.presentation.controllers.find_all_users_with_pagination_controller import FindAllUsersWithPaginationController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def find_all_users_with_pagination_composer() -> Callable[[HttpRequest], HttpResponse]:
    return FindAllUsersWithPaginationController(
        find_all_users_with_pagination_case=FindAllUsersWithPagination(
            user_repository=UserRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        )
    ).handle
