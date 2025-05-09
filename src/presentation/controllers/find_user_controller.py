from src.domain.use_cases.i_find_user import IFindUser
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.domain.value_objects.cpf import CPF

class FindUserController(ControllerInterface):

    def __init__(self, find_user_case:IFindUser) -> None:
        self.__find_user_case = find_user_case
    
    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            body = http_request.body
            cpf = CPF(body['user_cpf'])
            user = self.__find_user_case.find(
                cpf=cpf
            )
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'User Founded',
                    'content': {
                        'cpf': user.cpf.value,
                        'email': user.email,
                        'role': user.role,
                        'created_at': user.created_at.strftime(r'%d/%m/%Y')
                    }
                }
            )
        except Exception as e:
            raise e from e