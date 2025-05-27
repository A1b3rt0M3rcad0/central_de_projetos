from src.domain.value_objects.email import Email
from src.domain.value_objects.cpf import CPF
from src.data.interface.i_user_repository import IUserRepository
from src.domain.use_cases.i_update_user_email import IUpdateUserEmail
from src.errors.use_cases.email_already_exists_error import EmailAlreadyExistsError

class UpdateUserEmail(IUpdateUserEmail):

    def __init__(self, user_repository:IUserRepository) -> None:
        self.__user_repository = user_repository
    
    def update(self, cpf:CPF, email:Email) -> None:
        try:
            self.__email_already_exists(email=email)

            update_params = {'email': email.email}
            self.__user_repository.update(
                cpf=cpf,
                update_params=update_params
            )
        except Exception as e:
            raise e from e
    
    def __email_already_exists(self, email:Email) -> None:
        try:
            existing_user = self.__user_repository.find_by_email(email=email)
            if existing_user:
                raise EmailAlreadyExistsError(message=f'Email "{email.email}" already exists')
        except Exception as e:
            raise e from e