from src.domain.value_objects.password import Password
from src.domain.value_objects.cpf import CPF
from src.data.interface.i_user_repository import IUserRepository
from src.domain.use_cases.i_update_user_password import IUpdateUserPassword
from src.security.hashedpassword_factory import hashedpassword_factory
from src.security.hashedpassword_factory_chk import hashedpassword_factory_chk
from src.errors.use_cases.invalid_password_error import InvalidPasswordError

class UpdateUserPassword(IUpdateUserPassword):

    def __init__(self, user_repository:IUserRepository) -> None:
        self.__user_repository = user_repository
    
    def update(self, cpf:CPF, password:Password) -> None:
        try:

            user = self.__user_repository.find(cpf=cpf)
            old_password = user.password
            old_salt = user.salt

            if hashedpassword_factory_chk(old_password, old_salt, password=password):
                raise InvalidPasswordError(message=f'The new password "{password.password}" is the same as the previous one')

            hashedpassword = hashedpassword_factory(password)
            hashedpassword_bytes = hashedpassword.hashed_password
            salt_bytes = hashedpassword.salt
            update_params = {'password': hashedpassword_bytes, 'salt': salt_bytes}
            self.__user_repository.update(
                cpf=cpf,
                update_params=update_params
            )
        except Exception as e:
            raise e from e