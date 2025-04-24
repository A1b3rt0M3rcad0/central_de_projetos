from src.domain.value_objects.password import Password
from src.domain.value_objects.cpf import CPF
from src.data.interface.i_user_repository import IUserRepository
from src.auth.auth_factory import auth_factory
from src.security.hashedpassword_factory_chk import hashedpassword_factory_chk
from src.domain.use_cases.i_login import ILogin
from datetime import datetime, timezone, timedelta
from src.errors.use_cases.user_not_found_error import UserNotFoundError
from src.errors.use_cases.invalid_password_error import InvalidPasswordError
import dotenv
import os


class Login(ILogin):

    def __init__(self, user_repository:IUserRepository) -> None:
        self.__user_repository = user_repository
    
    def check(self, cpf:CPF, password:Password) -> str:
        try:
            result = self.__user_repository.find(
                cpf=cpf
            )
            user_password = result.password
            user_salt = result.salt
            chk_result = hashedpassword_factory_chk(user_password, user_salt, password)
            if chk_result:
                encrypt = auth_factory()
                dotenv.load_dotenv()
                hours = os.getenv('EXPIRE_TIME_TOKEN')
                if not hours.isnumeric():
                    raise ValueError(f'The {hours} is not a number')
                hours = float(hours)
                return encrypt.encode(
                    {
                        'cpf': result.cpf,
                        'role': result.role,
                        'exp': datetime.now(timezone.utc) + timedelta(hours=hours)
                    }
                )
            raise InvalidPasswordError(
                message=f'The password {password} is incorrect'
            )
        except AttributeError as e:
            raise UserNotFoundError(
                message=f'The user with this cpf: {cpf.value} does not exists'
            ) from e
        except Exception as e:
            raise e from e
