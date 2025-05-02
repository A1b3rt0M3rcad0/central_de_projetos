from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.domain.use_cases.i_login import ILogin
from src.domain.use_cases.i_create_refresh_token import ICreateRefreshToken
from src.domain.value_objects.password import Password
from src.domain.value_objects.cpf import CPF
from src.presentation.interface.controller_interface import ControllerInterface

class LoginController(ControllerInterface):

    def __init__(self, login_case:ILogin, create_refresh_token:ICreateRefreshToken) -> None:
        self.__login_case = login_case
        self.__create_refresh_token = create_refresh_token
    
    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            body = http_request.body
            cpf = CPF(body['cpf'])
            password = Password(body['password'])
            token  = self.__login_case.check(
                cpf=cpf,
                password=password
            )
            self.__create_refresh_token.create(
                cpf=cpf
            )
            return HttpResponse(
                status_code=200,
                body={
                    'token': token
                }
            )
        except Exception as e:
            raise e from e