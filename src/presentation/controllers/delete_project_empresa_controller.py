from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.domain.use_cases.i_delete_project_empresa import IDeleteProjectEmpresa

class DeleteProjectEmpresaController(ControllerInterface):

    def __init__(self, delete_project_empresa_case:IDeleteProjectEmpresa) -> None:
        self.__delete_project_empresa_case = delete_project_empresa_case
    
    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            body = http_request.body
            empresa_id = body['empresa_id']
            project_id = body['project_id']
            self.__delete_project_empresa_case.delete(
                empresa_id=empresa_id,
                project_id=project_id
            )
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'Project Empresa Deleted'
                }
            )
        except Exception as e:
            raise e from e