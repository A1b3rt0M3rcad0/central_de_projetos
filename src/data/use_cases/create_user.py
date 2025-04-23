#pylint:disable=all
from src.domain.value_objects.cpf import CPF
from src.domain.value_objects.email import Email
from src.domain.value_objects.password import Password
from src.domain.value_objects.roles import Role
from src.domain.use_cases.i_create_user import ICreateUser
from src.data.interface.i_user_repository import IUserRepository

class CreateUser(ICreateUser):

    def __init__(self, user_repository:IUserRepository) -> None:
        self.__user_repository = user_repository

    def create(self, cpf:CPF, email:Email, role:Role, password:Password) -> None:
        self.__user_repository

        