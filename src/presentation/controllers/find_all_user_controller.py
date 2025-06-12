#pylint:disable=W0612
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.domain.use_cases.i_find_all_user import IFindAllUser

class FindAllUserController(ControllerInterface):

    def __init__(self, find_all_user_case:IFindAllUser) -> None:
        self.__find_all_user_case = find_all_user_case
    
    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            body = http_request.body
            result = self.__find_all_user_case.find()
            return HttpResponse(
                status_code=200,
                body={
                    "message": "Users Founded",
                    "content": [
                        {
                            "name": user.name,
                            "cpf": user.cpf.value,
                            "email": user.email.email,
                            "role": user.role.value,
                            "created_at": user.created_at.strftime(r'%d/%m/%Y')
                        }
                        for user in result
                    ]
                }
            )
        except Exception as e:
            raise e from e