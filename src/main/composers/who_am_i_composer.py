from src.presentation.controllers.who_am_i_controller import WhoAmIController
from src.data.use_cases.decode_jwt_token import DecodeJwtToken
from src.data.use_cases.find_user import FindUser
from src.infra.relational.repository.user_repository import UserRepository
from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.auth.auth_factory import auth_factory
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def who_am_i_composer() -> Callable[[HttpRequest], HttpResponse]:
    return WhoAmIController(
        decode_jwt_token_case=DecodeJwtToken(
            encrypt=auth_factory()
        ),
        find_user_case=FindUser(
            user_repository=UserRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        )
    ).handle