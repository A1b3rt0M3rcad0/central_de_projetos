from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.infra.relational.repository.refresh_token_repository import RefreshTokenRepository
from src.data.use_cases.update_refresh_token import UpdateRefreshToken
from src.presentation.controllers.update_refresh_token_controller import UpdateRefreshTokenController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from typing import Callable

def update_refresh_token_composer() -> Callable[[HttpRequest], HttpResponse]:
    return UpdateRefreshTokenController(
        update_refresh_token_case=UpdateRefreshToken(
            refresh_token_repository=RefreshTokenRepository(
                db_connection_handler=db_connection_handler_factory()
            )
        )
    ).handle