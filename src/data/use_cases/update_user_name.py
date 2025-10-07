from src.domain.value_objects.cpf import CPF
from src.data.interface.i_user_repository import IUserRepository
from src.domain.use_cases.i_update_user_name import IUpdateUserName

class UpdateUserName(IUpdateUserName):

    def __init__(self, user_repository:IUserRepository) -> None:
        self.__user_repository = user_repository
    
    def update(self, cpf:CPF, name:str) -> None:
        try:
            if not name or len(name.strip()) < 3:
                raise ValueError("Nome deve ter pelo menos 3 caracteres")
            
            update_params = {'name': name.strip()}
            self.__user_repository.update(
                cpf=cpf,
                update_params=update_params
            )
        except Exception as e:
            raise e from e

