from src.domain.use_cases.i_find_all_projects_from_empresa import IFindAllProjectsfromEmpresa
from src.domain.use_cases.i_find_project import IFindProject
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

class FindAllProjectsFromEmpresaController(ControllerInterface):

    def __init__(self, find_all_projects_from_empresa_case:IFindAllProjectsfromEmpresa, find_project_case:IFindProject) -> None:
        self.__find_all_projects_from_empresa_case = find_all_projects_from_empresa_case
        self.__find_project_case = find_project_case

    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            path_params = http_request.path_params
            empresa_id = path_params['empresa_id']
            project_empresa_results = self.__find_all_projects_from_empresa_case.find(
                empresa_id=empresa_id
            )
            projects = [self.__find_project_case.find(project_id=project_empresa.project_id)
                        for project_empresa in project_empresa_results
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