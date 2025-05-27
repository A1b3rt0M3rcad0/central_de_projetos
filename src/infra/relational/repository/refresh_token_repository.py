from src.infra.relational.models.refresh_token import RefreshToken
from src.infra.relational.config.interface.i_db_connection_handler import IDBConnectionHandler
from src.domain.value_objects.cpf import CPF
from src.domain.entities.refresh_token import RefreshTokenEntity
from src.data.interface.i_refresh_token_repository import IRefreshTokenRepository

# Errors
from src.errors.repository.already_exists_error.refresh_token_already_exists import RefreshTokenAlreadyExists
from src.errors.repository.not_exists_error.refresh_token_not_exists import RefreshTokenNotExists
from src.errors.repository.error_on_insert.error_on_insert_refresh_token import ErrorOnInsertRefreshToken
from src.errors.repository.error_on_find.error_on_find_refresh_token import ErrorOnFindRefreshToken
from src.errors.repository.error_on_update.error_on_update_refresh_token import ErrorOnUpdateRefreshToken
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

class RefreshTokenRepository(IRefreshTokenRepository):

    def __init__(self, db_connection_handler:IDBConnectionHandler) -> None:
        self.__db_connection_handler  = db_connection_handler
    
    def insert(self, user_cpf:CPF, token:str) -> None:
        try:
            user_cpf_entry = user_cpf.value
            with self.__db_connection_handler as db:
                refresh_token = RefreshToken(
                    user_cpf=user_cpf_entry,
                    token=token
                )
                db.session.add(
                    refresh_token
                )
                db.session.commit()
        except IntegrityError as e:
            raise RefreshTokenAlreadyExists(
                message=f'Refresh Token from cpf "{user_cpf_entry}" Registry already exists: {e}'
            ) from e
        except SQLAlchemyError as e:
            raise e
        except Exception as e:
            raise ErrorOnInsertRefreshToken(
                message=f'Error on insert refresh token user_cpf={user_cpf}, token={token}: {str(e)}'
            ) from e
    
    def find(self, user_cpf:CPF) -> RefreshTokenEntity:
        try:
            user_cpf_entry = user_cpf.value
            with self.__db_connection_handler as db:
                result = db.session.query(RefreshToken).where(
                    RefreshToken.user_cpf == user_cpf_entry
                ).first()
                if result is None:
                    raise RefreshTokenNotExists(f'refresh token from cpf {user_cpf_entry} does not exists')
                return RefreshTokenEntity(
                    cpf=user_cpf_entry,
                    token=result.token
                )
        except Exception as e:
            raise ErrorOnFindRefreshToken(
                message=f'Error on find refresh token from user_cpf={user_cpf}: {str(e)}'
            ) from e
    
    def update(self, user_cpf:CPF, new_token:str) -> None:
        try:
            user_cpf_entry = user_cpf.value
            with self.__db_connection_handler as db:
                db.session.query(RefreshToken).where(RefreshToken.user_cpf == user_cpf_entry).update(
                    {'token': new_token}
                )
                db.session.commit()
        except SQLAlchemyError as e:
            raise RefreshTokenNotExists(f'The token from cpf: "{user_cpf_entry}" does not exists: {e}') from e
        except Exception as e:
            raise ErrorOnUpdateRefreshToken(
                message=f'Error on update refresh token from user_cpf={user_cpf} to token={new_token}: {str(e)}'
            ) from e