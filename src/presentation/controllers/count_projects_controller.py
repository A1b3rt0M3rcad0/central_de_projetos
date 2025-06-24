from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.domain.use_cases.i_count_projects import ICountProjects

class CountProjectsController(ControllerInterface):

    def __init__(self, count_projects:ICountProjects) -> None:
        self.__count_projects = count_projects
    
    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'Count Projects',
                    'content': self.__count_projects.count()
                }
            )
        except Exception as e:
            raise e from e