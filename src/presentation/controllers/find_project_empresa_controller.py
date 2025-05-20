from src.domain.use_cases.i_find_project_empresa import IFindProjectEmpresa
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

class FindProjectEmpresaController(ControllerInterface):

    def __init__(self, find_project_empresa_case:IFindProjectEmpresa) -> None:
        self.__find_project_empresa_case = find_project_empresa_case
    
    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            path_params = http_request.path_params
            project_id = path_params['project_id']
            empresa_id = path_params['empresa_id']
            project_empresa = self.__find_project_empresa_case.find(
                empresa_id=empresa_id,
                project_id=project_id
            )
            return HttpResponse(
                status_code=200,
                body={
                    'empresa_id': project_empresa.empresa_id,
                    'project_id': project_empresa.project_id,
                    'created_at': project_empresa.created_at.strftime(r'%d/%m/%Y')
                }
            )
        except Exception as e:
            raise e from e