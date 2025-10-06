from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.user_repository import UserRepository
from src.data.use_cases.find_all_users_with_pagination_and_filter import FindAllUsersWithPaginationAndFilter
from src.presentation.controllers.find_all_users_with_pagination_and_filter_controller import FindAllUsersWithPaginationAndFilterController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def find_all_users_with_pagination_and_filter_composer() -> Callable[[HttpRequest], HttpResponse]:
    """Composer para o caso de uso de buscar usuários com paginação e filtro."""
    
    return FindAllUsersWithPaginationAndFilterController(
        find_all_users_with_pagination_and_filter_case=FindAllUsersWithPaginationAndFilter(
            user_repository=UserRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        )
    ).handle
