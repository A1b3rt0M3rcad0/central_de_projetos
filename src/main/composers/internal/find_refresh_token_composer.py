from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory
from src.data.use_cases.find_refresh_token import FindRefreshToken
from src.infra.relational.repository.refresh_token_repository import RefreshTokenRepository

def find_refresh_token_internal_composer() -> FindRefreshToken:
    return FindRefreshToken(
        refresh_token_repository=RefreshTokenRepository(
            db_connection_handler=db_connection_handler_factory()
        )
    )