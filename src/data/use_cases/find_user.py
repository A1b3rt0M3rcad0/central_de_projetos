from src.domain.entities.user import UserEntity
from src.domain.value_objects.cpf import CPF
from src.domain.use_cases.i_find_user import IFindUser
from src.data.interface.i_user_repository import IUserRepository
from src.errors.use_cases.user_not_found_error import UserNotFoundError

class FindUser(IFindUser):

    def __init__(self, user_repository:IUserRepository) -> None:
        self.__user_repository = user_repository
    
    def find(self, cpf:CPF) -> UserEntity:
        try:
            result = self.__user_repository.find(
                cpf=cpf
            )
            return result
        except AttributeError as e:
            raise UserNotFoundError(message=f'User with this cpf: {cpf.value} not founded') from e
        except Exception as e:
            raise e from e