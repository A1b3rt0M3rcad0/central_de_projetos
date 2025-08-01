from src.domain.use_cases.i_create_refresh_token_fiscal import ICreateRefreshTokenFiscal
from src.data.interface.i_fiscal_repository import IFiscalRepository
from src.domain.value_objects.email import Email
from src.auth.auth_factory import auth_factory
import dotenv
import os
from datetime import datetime, timedelta, timezone

class CreateRefreshTokenFiscal(ICreateRefreshTokenFiscal):

    def __init__(self, fiscal_repository: IFiscalRepository) -> None:
        self.__fiscal_repository = fiscal_repository

    def create(self, email: Email) -> None:
        try:
            refresh_token = self.generate_token(email)
            # Find the fiscal by email to get the fiscal_id
            fiscal = self.__fiscal_repository.find_by_email(email)
            self.__fiscal_repository.insert_refresh_token(
                fiscal_id=fiscal.fiscal_id,
                refresh_token=refresh_token
            )
        except Exception as e:
            raise e from e
    
    def generate_token(self, email: Email) -> str:
        dotenv.load_dotenv()
        expire_time_refresh_token = os.getenv('EXPIRE_TIME_REFRESH_TOKEN')
        if expire_time_refresh_token is None or not expire_time_refresh_token.replace('.', '', 1).isdigit():
            raise ValueError(f'The EXPIRE_TIME_REFRESH_TOKEN value is invalid: {expire_time_refresh_token}')
        expire_time_refresh_token = float(expire_time_refresh_token)
        exp = datetime.now(timezone.utc) + timedelta(days=float(expire_time_refresh_token))
        encrypt = auth_factory()
        refresh_token = encrypt.encode(
                {
                    'email': email.email,
                    'exp': exp
                }
            )
        return refresh_token 