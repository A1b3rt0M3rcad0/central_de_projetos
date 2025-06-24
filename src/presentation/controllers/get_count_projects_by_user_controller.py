from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.domain.use_cases.i_get_count_projects_by_user import IGetCountProjectsByuser

class GetCountProjectsByUserController(ControllerInterface):

    def __init__(self, get_count_projects_by_user:IGetCountProjectsByuser) -> None:
        self.__get_count_projects_by_user = get_count_projects_by_user
    
    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'Count Projects By user',
                    'content': self.__get_count_projects_by_user.get()
                }
            )
        except Exception as e:
            raise e from e