from src.domain.use_cases.i_update_refresh_token import IUpdateRefreshToken
from src.domain.value_objects.cpf import CPF
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

class UpdateRefreshTokenController(ControllerInterface):

    def __init__(self, update_refresh_token_case:IUpdateRefreshToken) -> None:
        self.__update_refresh_token_case = update_refresh_token_case
    
    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            body = http_request.body
            cpf = body['cpf']
            token = body['token']
            self.__update_refresh_token_case.update(
                user_cpf=CPF(cpf),
                new_token=token
            )
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'refresh token updated'
                }
            )
        except Exception as e:
            raise e from e