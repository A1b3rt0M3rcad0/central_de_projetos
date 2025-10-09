from src.domain.value_objects.password import Password
from src.domain.value_objects.email import Email
from src.data.interface.i_fiscal_repository import IFiscalRepository
from src.auth.auth_factory import auth_factory
from src.security.hashedpassword_factory_chk import hashedpassword_factory_chk
from src.domain.use_cases.i_login_fiscal import ILoginFiscal
from datetime import datetime, timezone, timedelta
from src.errors.use_cases.fiscal_not_found_error import FiscalNotFoundError
from src.errors.use_cases.invalid_password_error import InvalidPasswordError
from src.errors.use_cases.fiscal_inactive_error import FiscalInactiveError
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
            
            # Verificar se o fiscal está ativo (NULL ou 1 = ativo, 0 = inativo)
            if result.is_active is not None and result.is_active == 0:
                raise FiscalInactiveError(
                    message='Sua conta de fiscal está inativa. Entre em contato com o administrador do sistema para reativá-la.'
                )
            
            fiscal_password = result.password
            fiscal_salt = result.salt
            chk_result = hashedpassword_factory_chk(fiscal_password, fiscal_salt, password)
            if chk_result:
                encrypt = auth_factory()
                dotenv.load_dotenv()
                
                # Configurações de tempo do token
                access_token_hours = float(os.getenv('EXPIRE_TIME_TOKEN', '48'))
                deadline_hours = float(os.getenv('EXPIRE_DEADLINE', '24'))
                
                current_time = datetime.now(timezone.utc)
                expiry = current_time + timedelta(hours=access_token_hours)
                deadline = current_time + timedelta(hours=deadline_hours)
                
                return encrypt.encode(
                    {
                        'email': result.email,
                        'role': 'fiscal',
                        'fiscal_id': result.fiscal_id,
                        'exp': int(expiry.timestamp()),
                        'deadline': int(deadline.timestamp())
                    }
                )
            raise InvalidPasswordError(
                message='Email ou senha incorretos. Verifique suas credenciais e tente novamente.'
            )
        except FiscalNotExists as e:
            raise FiscalNotFoundError(
                message='Email ou senha incorretos. Verifique suas credenciais e tente novamente.'
            ) from e
        except AttributeError as e:
            # This might happen if the fiscal exists but doesn't have required fields
            raise FiscalNotFoundError(
                message='Email ou senha incorretos. Verifique suas credenciais e tente novamente.'
            ) from e
        except Exception as e:
            raise e from e 