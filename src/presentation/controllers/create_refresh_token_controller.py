from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.domain.use_cases.i_create_refresh_token import ICreateRefreshToken
from src.presentation.interface.controller_interface import ControllerInterface

class CreateRefreshTokenController(ControllerInterface):

    def __init__(self, create_refresh_token_case:ICreateRefreshToken) ->  None:
        self.__create_refresh_token_case = create_refresh_token_case
    
    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            body = http_request.body
            cpf = body['cpf']
            self.__create_refresh_token_case.create(
                cpf=cpf
            )
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'Refresh Token Created'
                }
            )
        except Exception as e:
            raise e from e