from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.refresh_token_repository import RefreshTokenRepository
from src.data.use_cases.find_refresh_token import FindRefreshToken
from src.presentation.controllers.find_refresh_token_controller import FindRefreshTokenController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def find_refresh_token_composer() -> Callable[[HttpRequest], HttpResponse]:
    return FindRefreshTokenController(
        find_refresh_token_case=FindRefreshToken(
            refresh_token_repository=RefreshTokenRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        )
    ).handle