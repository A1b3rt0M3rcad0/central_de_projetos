from src.data.interface.i_user_repository import IUserRepository
from src.domain.use_cases.i_delete_user import IDeleteUser
from src.domain.value_objects.cpf import CPF

class DeleteUser(IDeleteUser):

    def __init__(self, user_repository:IUserRepository) -> None:
        self.__user_repository = user_repository
    
    def delete(self, cpf:CPF) -> None:
        try:
            self.__user_repository.delete(
                cpf=cpf
            )
        except Exception as e:
            raise e from e