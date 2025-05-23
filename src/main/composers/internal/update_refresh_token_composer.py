from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.data.use_cases.update_refresh_token import UpdateRefreshToken
from src.infra.relational.repository.refresh_token_repository import RefreshTokenRepository

def update_refresh_token_internal_composer() -> UpdateRefreshToken:
    return UpdateRefreshToken(
        refresh_token_repository=RefreshTokenRepository(
            db_connection_handler=db_connection_handler_factory
        )
    )