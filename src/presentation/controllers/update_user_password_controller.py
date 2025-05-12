from src.domain.use_cases.i_update_user_password import IUpdateUserPassword
from src.domain.value_objects.password import Password
from src.domain.value_objects.cpf import CPF
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

class UpdateUserPassword(ControllerInterface):

    def __init__(self, update_user_password_case:IUpdateUserPassword) -> None:
        self.__update_user_password_case = update_user_password_case
    
    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            body = http_request.body
            cpf = body['cpf']
            password = body['password']
            self.__update_user_password_case.update(
                cpf = CPF(cpf),
                password=Password(password)
            )
        except Exception as e:
            raise e from e