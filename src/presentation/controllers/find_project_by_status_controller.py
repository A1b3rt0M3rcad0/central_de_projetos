from src.domain.use_cases.i_find_project_by_status import IFindProjectByStatus
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.presentation.interface.controller_interface import ControllerInterface

class FindProjectByStatusController(ControllerInterface):

    def __init__(self, find_project_by_status_case:IFindProjectByStatus) -> None:
        self.__find_project_by_status_case = find_project_by_status_case
    
    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            body = http_request.body
            status_id = body['status_id']
            projects = self.__find_project_by_status_case.find(
                status_id=status_id
            )
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'Projects Founded',
                    'content': [
                        {'id': project.project_id,
                         'status_id': project.status_id,
                         'verba_disponivel': project.verba_disponivel,
                         'andamento_do_projeto': project.andamento_do_projeto,
                         'start_date': project.start_date.strftime(r'%d/%m/%Y'),
                         'expected_completion_date': project.expected_completion_date.strftime(r'%d/%m/%Y'),
                         'end_date': project.end_date.strftime(r'%d/%m/%Y'),
                         'name': project.name}
                        for project in projects
                    ]
                }
            )
        except Exception as e:
            raise e from e