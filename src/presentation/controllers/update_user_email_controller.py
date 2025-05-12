from src.domain.use_cases.i_update_user_email import IUpdateUserEmail
from src.domain.value_objects.cpf import CPF
from src.domain.value_objects.email import Email
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

class UpdateuserEmailController(ControllerInterface):

    def __init__(self, update_user_email_case:IUpdateUserEmail) -> None:
        self.__update_user_email_case = update_user_email_case
    
    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            body = http_request.body
            email = body['email']
            cpf = body['cpf']
            self.__update_user_email_case.update(
                cpf=CPF(cpf),
                email=Email(email)
            )
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'user email updated'
                }
            )
        except Exception as e:
            raise e from e