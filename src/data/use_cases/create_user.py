from src.domain.value_objects.cpf import CPF
from src.domain.value_objects.email import Email
from src.domain.value_objects.password import Password
from src.domain.value_objects.roles import Role
from src.domain.use_cases.i_create_user import ICreateUser
from src.data.interface.i_user_repository import IUserRepository
from src.errors.repository.already_exists_error.user_already_exists import UserAlreadyExists
from src.errors.use_cases.create_user_error import CreateUserError
from src.security.hashedpassword_factory import hashedpassword_factory
from src.security.cryptography.utils.salt import Salt
from typing import Optional

class CreateUser(ICreateUser):

    def __init__(self, user_repository:IUserRepository) -> None:
        self.__user_repository = user_repository

    def create(self, cpf:CPF, email:Email, role:Role, password:Password, name:Optional[str]=None) -> None:
        hashedpassword = hashedpassword_factory(password)
        salt = Salt(hashedpassword.salt)
        try:
            self.__user_repository.insert(
                cpf=cpf,
                email=email,
                role=role,
                password=hashedpassword,
                salt=salt,
                name=name
            )
        except UserAlreadyExists as e:
            raise CreateUserError(
                message=f'Error on create user: {e.message}'
            ) from e