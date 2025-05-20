from src.domain.use_cases.i_find_all_projects_from_empresa import IFindAllProjectsfromEmpresa
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

class FindAllProjectsFromEmpresaController(ControllerInterface):

    def __init__(self, find_all_projects_from_empresa_case:IFindAllProjectsfromEmpresa) -> None:
        self.__find_all_projects_from_empresa_case = find_all_projects_from_empresa_case

    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            path_params = http_request.path_params
            empresa_id = path_params['empresa_id']
            project_empresa_list = self.__find_all_projects_from_empresa_case.find(
                empresa_id=empresa_id
            )
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'Projects from empresa founded',
                    'content': [
                        {
                            'project_id': project_empresa.project_id,
                            'empresa_id': project_empresa.empresa_id,
                            'created_at': project_empresa.created_at.strftime(r'%d/$m/%Y')
                        }
                        for project_empresa in project_empresa_list
                    ]
                }
            )
        except Exception as e:
            raise e from e