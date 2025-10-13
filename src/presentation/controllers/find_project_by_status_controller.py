from src.domain.use_cases.i_find_project_by_status import IFindProjectByStatus
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.presentation.interface.controller_interface import ControllerInterface

class FindProjectByStatusController(ControllerInterface):

    def __init__(self, find_project_by_status_case:IFindProjectByStatus) -> None:
        self.__find_project_by_status_case = find_project_by_status_case
    
    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            path_params = http_request.path_params
            status_id = path_params['status_id']
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
                         'verba_disponivel': float(project.verba_disponivel) if project.verba_disponivel else None,
                         'andamento_do_projeto': project.andamento_do_projeto,
                         'start_date': project.start_date.strftime(r'%d/%m/%Y') if project.start_date else None,
                         'expected_completion_date': project.expected_completion_date.strftime(r'%d/%m/%Y') if project.expected_completion_date else None,
                         'end_date': project.end_date.strftime(r'%d/%m/%Y') if project.end_date else None,
                         'name': project.name}
                        for project in projects
                    ]
                }
            )
        except Exception as e:
            raise e from e