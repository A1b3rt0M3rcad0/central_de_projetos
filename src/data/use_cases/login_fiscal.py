from src.domain.value_objects.password import Password
from src.domain.value_objects.email import Email
from src.data.interface.i_fiscal_repository import IFiscalRepository
from src.auth.auth_factory import auth_factory
from src.security.hashedpassword_factory_chk import hashedpassword_factory_chk
from src.domain.use_cases.i_login_fiscal import ILoginFiscal
from datetime import datetime, timezone, timedelta
from src.errors.use_cases.fiscal_not_found_error import FiscalNotFoundError
from src.errors.use_cases.invalid_password_error import InvalidPasswordError
from src.errors.repository.not_exists_error.fiscal_not_exists import FiscalNotExists
import dotenv
import os


class LoginFiscal(ILoginFiscal):

    def __init__(self, fiscal_repository:IFiscalRepository) -> None:
        self.__fiscal_repository = fiscal_repository
    
    def check(self, email:Email, password:Password) -> str:
        try:
            result = self.__fiscal_repository.find_by_email(
                email=email
            )
            fiscal_password = result.password
            fiscal_salt = result.salt
            chk_result = hashedpassword_factory_chk(fiscal_password, fiscal_salt, password)
            if chk_result:
                encrypt = auth_factory()
                dotenv.load_dotenv()
                hours = os.getenv('EXPIRE_TIME_TOKEN')
                if hours is None or not hours.replace('.', '', 1).isdigit():
                    raise ValueError(f'The EXPIRE_TIME_TOKEN value is invalid: {hours}')
                hours = float(hours)
                return encrypt.encode(
                    {
                        'email': result.email,
                        'role': 'fiscal',
                        'exp': datetime.now(timezone.utc) + timedelta(hours=hours)
                    }
                )
            raise InvalidPasswordError(
                message=f'The password {password} is incorrect'
            )
        except FiscalNotExists as e:
            raise FiscalNotFoundError(
                message=f'The fiscal with this email: {email.email} does not exists'
            ) from e
        except AttributeError as e:
            # This might happen if the fiscal exists but doesn't have required fields
            raise FiscalNotFoundError(
                message=f'The fiscal with this email: {email.email} does not exists or has invalid data'
            ) from e
        except Exception as e:
            raise e from e 