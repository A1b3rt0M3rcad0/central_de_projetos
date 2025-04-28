from src.infra.relational.models.refresh_token import RefreshToken
from src.infra.relational.config.interface.i_db_connection_handler import IDBConnectionHandler
from src.domain.value_objects.cpf import CPF
from src.domain.entities.refresh_token import RefreshTokenEntity
from src.errors.repository.refresh_token_already_exists import RefreshTokenAlreadyExists
from src.errors.repository.refresh_token_not_exists import RefreshTokenNotExists
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

class RefreshTokenRepository:

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
            raise e
    
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
            raise e