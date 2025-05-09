from src.domain.use_cases.i_delete_user import IDeleteUser
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.domain.value_objects.cpf import CPF

class DeleteUserController(ControllerInterface):

    def __init__(self, delete_user_case:IDeleteUser) -> None:
        self.__delete_user_case = delete_user_case
    
    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            body = http_request.body
            cpf = CPF(body['cpf'])
            self.__delete_user_case.delete(
                cpf = cpf
            )
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'User Deleted'
                }
            )
        except Exception as e:
            raise e from e