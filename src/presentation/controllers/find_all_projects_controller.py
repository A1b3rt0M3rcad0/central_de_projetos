#pylint:disable=all
from src.domain.use_cases.i_find_all_project import IFindAllProjects
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

class FindAllProjectsController(ControllerInterface):

    def __init__(self, find_all_projects_case:IFindAllProjects) -> None:
        self.__find_all_projects_case = find_all_projects_case
    
    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            body = http_request.body
            results = self.__find_all_projects_case.find()
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'Projects Founded',
                    'content': [
                        [project.project_id,
                         project.status_id,
                         project.verba_disponivel,
                         project.andamento_do_projeto,
                         project.start_date,
                         project.expected_completion_date,
                         project.end_date,
                         project.name]
                        for project in results
                    ]
                }
            )
        except Exception as e:
            raise e from e