from src.domain.use_cases.i_create_refresh_token import ICreateRefreshToken
from src.data.interface.i_refresh_token_repository import IRefreshTokenRepository
from src.domain.value_objects.cpf import CPF
from src.auth.auth_factory import auth_factory
import dotenv
import os
from datetime import datetime, timedelta, timezone

class CreateRefreshToken(ICreateRefreshToken):

    def __init__(self, refresh_token_repository:IRefreshTokenRepository) -> None:
        self.__refresh_token_repository = refresh_token_repository

    def create(self, cpf:CPF) -> None:
        try:
            refresh_token = self.generate_token(cpf)
            self.__refresh_token_repository.insert(
                user_cpf=cpf,
                token=refresh_token
            )
        except Exception as e:
            raise e from e
    
    def generate_token(self, cpf:CPF) -> str:
        dotenv.load_dotenv()
        expire_time_refresh_token = os.getenv('EXPIRE_TIME_REFRESH_TOKEN')
        if expire_time_refresh_token is None or not expire_time_refresh_token.replace('.', '', 1).isdigit():
            raise ValueError(f'The EXPIRE_TIME_REFRESH_TOKEN value is invalid: {expire_time_refresh_token}')
        expire_time_refresh_token = float(expire_time_refresh_token)
        exp = datetime.now(timezone.utc) + timedelta(days=float(expire_time_refresh_token))
        encrypt = auth_factory()
        refresh_token = encrypt.encode(
                {
                    'cpf': cpf.value,
                    'exp': exp
                }
            )
        return refresh_token