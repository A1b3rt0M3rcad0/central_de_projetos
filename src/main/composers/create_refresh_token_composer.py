from src.data.use_cases.create_refresh_token import CreateRefreshToken
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.infra.relational.repository.refresh_token_repository import RefreshTokenRepository
from src.presentation.controllers.create_refresh_token_controller import CreateRefreshTokenController
from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from typing import Callable

def create_refresh_token_composer() -> Callable[[HttpRequest], HttpResponse]:
    return CreateRefreshTokenController(
        create_refresh_token_case=CreateRefreshToken(
            refresh_token_repository=RefreshTokenRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        )
    ).handle