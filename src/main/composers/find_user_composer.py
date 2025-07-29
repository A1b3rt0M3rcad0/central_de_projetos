"""
Composer responsável por montar a cadeia de dependências para o endpoint de busca de usuário.

Retorna o handler do controller, que recebe um HttpRequest e retorna um HttpResponse.

Fluxo:
- Instancia UserRepository com o handler de conexão
- Instancia o use case FindUser
- Instancia o controller FindUserController
- Retorna o método handle do controller
"""

from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.user_repository import UserRepository
from src.data.use_cases.find_user import FindUser
from src.presentation.controllers.find_user_controller import FindUserController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def find_user_composer() -> Callable[[HttpRequest], HttpResponse]:
    return FindUserController(
        find_user_case=FindUser(
            user_repository=UserRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        )
    ).handle