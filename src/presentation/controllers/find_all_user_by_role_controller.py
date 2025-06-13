from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.domain.use_cases.i_find_all_user_by_role import IFindAllUserByRole
from src.domain.value_objects.roles import Role

class FindAllUserByRoleController(ControllerInterface):

    def __init__(self, find_all_user_by_role_case:IFindAllUserByRole) -> None:
        self.__find_all_user_by_role_case = find_all_user_by_role_case
    
    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            path_params = http_request.path_params
            role = path_params["role"]
            result = self.__find_all_user_by_role_case.find(role=Role(role=role))
            return HttpResponse(
                status_code=200,
                body={
                    "message": "Users Founded",
                    "content": [{
                        "cpf": user.cpf.value,
                        "name": user.name,
                        "email": user.email.email,
                        "role": user.role.value,
                        "created_at": user.created_at.strftime(r"%d/%m/%Y")
                    } for user in result]
                }
            )
        except Exception as e:
            raise e from e