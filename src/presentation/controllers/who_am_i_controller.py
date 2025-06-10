from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.domain.use_cases.i_decode_jwt_token import IDecodeJwtToken
from src.domain.use_cases.i_find_user import IFindUser
from src.domain.value_objects.cpf import CPF

class WhoAmIController(ControllerInterface):

    def __init__(self, decode_jwt_token_case:IDecodeJwtToken, find_user_case:IFindUser) -> None:
        self.__decode_jwt_token_case = decode_jwt_token_case
        self.__find_user_case = find_user_case
    
    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            path_params = http_request.path_params
            jwt = path_params["token"]
            result = self.__decode_jwt_token_case.decode(jwt)
            cpf = result["cpf"]
            user = self.__find_user_case.find(cpf=CPF(cpf))
            return HttpResponse(
                status_code=200,
                body={
                    "message" : "You are founded",
                    "content": {
                        "name": user.name,
                        "role": user.role.value
                    }
                }
            )
        except Exception as e:
            raise e from e