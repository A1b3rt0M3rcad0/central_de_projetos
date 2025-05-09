from src.domain.use_cases.i_find_all_projects_from_fiscal import IFindAllProjectsFromFiscal
from src.domain.use_cases.i_find_project import IFindProject
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.presentation.interface.controller_interface import ControllerInterface

class FindAllProjectsFromFiscal(ControllerInterface):

    def __init__(self, find_all_projects_from_fiscal_case:IFindAllProjectsFromFiscal, find_project_case:IFindProject) -> None:
        self.__find_all_projects_from_fiscal_case = find_all_projects_from_fiscal_case
        self.__find_project_case = find_project_case

    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            body = http_request['body']
            fiscal_id = body['fiscal_id']
            project_fiscal_results = self.__find_all_projects_from_fiscal_case.find(fiscal_id=fiscal_id)
            projects = [self.__find_project_case.find(project_id=project_bairro.project_id)
                        for project_bairro in project_fiscal_results
                        ]
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'Projects Founded',
                    'content': {[
                        [project.project_id,
                         project.status_id,
                         project.verba_disponivel,
                         project.andamento_do_projeto,
                         project.start_date,
                         project.expected_completion_date,
                         project.end_date,
                         project.name]
                        for project in projects
                    ]}
                }
            )
        except Exception as e:
            raise e from e