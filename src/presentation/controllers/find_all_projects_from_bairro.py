from src.domain.use_cases.i_find_all_projects_from_bairro import IFindAllProjectsFromBairro
from src.domain.use_cases.i_find_project import IFindProject
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

class FindAllProjectsFromBairro(ControllerInterface):

    def __init__(self, find_all_projects_from_bairro_case:IFindAllProjectsFromBairro, find_project_case:IFindProject) -> None:
        self.__find_all_projects_from_bairro_case = find_all_projects_from_bairro_case
        self.__find_project_case = find_project_case
    
    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            body = http_request.body
            bairro_id = body['bairro_id']
            project_bairro_results = self.__find_all_projects_from_bairro_case.find(bairro_id=bairro_id)
            projects = [self.__find_project_case.find(project_id=project_bairro.project_id)
                        for project_bairro in project_bairro_results
                        ]
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'Projects Founded',
                    'content': [
                        {'id': project.project_id,
                         'status_id': project.status_id,
                         'verba_disponivel': project.verba_disponivel,
                         'andamento_do_projeto': project.andamento_do_projeto,
                         'start_date': project.start_date,
                         'expected_completion_date': project.expected_completion_date,
                         'end_date': project.end_date,
                         'name': project.name}
                        for project in projects
                    ]
                }
            )
        except Exception as e:
            raise e from e