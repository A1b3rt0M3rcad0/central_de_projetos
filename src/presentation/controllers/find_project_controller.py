from src.domain.use_cases.i_find_project import IFindProject
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.presentation.interface.controller_interface import ControllerInterface

class FindProjectController(ControllerInterface):

    def __init__(self, find_project_case:IFindProject) -> None:
        self.__find_project_case = find_project_case
    
    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            path_params = http_request.path_params
            project_id = path_params['project_id']
            project = self.__find_project_case.find(project_id=project_id)
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'Project Founded',
                    'content': {
                        'id': project.project_id,
                        'status_id': project.status_id,
                        'verba_disponivel': project.verba_disponivel,
                        'andamento_do_projeto': project.andamento_do_projeto,
                        'start_date': project.start_date.strftime(r'%d/%m/%Y') if project.start_date else project.start_date,
                        'expected_completion_date': project.expected_completion_date.strftime(r'%d/%m/%Y') if project.expected_completion_date else project.expected_completion_date,
                        'end_date': project.end_date.strftime(r'%d/%m/%Y') if project.end_date else project.end_date,
                        'name': project.name
                        }
                }
            )
        except Exception as e:
            raise e from e