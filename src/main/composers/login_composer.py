from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.refresh_token_repository import RefreshTokenRepository
from src.infra.relational.repository.user_repository import UserRepository
from src.data.use_cases.login import Login
from src.data.use_cases.create_refresh_token import CreateRefreshToken
from src.data.use_cases.update_refresh_token import UpdateRefreshToken
from src.presentation.controllers.login_controller import LoginController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def login_composer() -> Callable[[HttpRequest], HttpResponse]:
    return LoginController(
        login_case=Login(
            user_repository=UserRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        ),
        create_refresh_token=CreateRefreshToken(
            refresh_token_repository=RefreshTokenRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        ),
        update_refresh_token=UpdateRefreshToken(
            refresh_token_repository=RefreshTokenRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        )
    ).handle