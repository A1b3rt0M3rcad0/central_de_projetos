from src.domain.use_cases.i_find_refresh_token import IFindRefreshToken
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.presentation.interface.controller_interface import ControllerInterface
from src.domain.value_objects.cpf import CPF

class FindRefreshTokenController(ControllerInterface):

    def __init__(self, find_refresh_token_case:IFindRefreshToken) -> None:
        self.__find_refresh_token_case = find_refresh_token_case
    
    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            query_params = http_request.query_params
            cpf = CPF(query_params['cpf'])
            result = self.__find_refresh_token_case.find(
                user_cpf=cpf
            )
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'Refresh token founded',
                    'content': {
                        'cpf': result.cpf,
                        'token': result.token
                    }
                }
            )
        except Exception as e:
            raise e from e