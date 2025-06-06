from src.domain.use_cases.i_create_project_empresa import ICreateProjectEmpresa
from src.domain.use_cases.i_create_history_project import ICreateHistoryProject
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

class CreateProjectEmpresaController(ControllerInterface):

    def __init__(self, create_project_empresa_case:ICreateProjectEmpresa, create_history_project_case:ICreateHistoryProject) -> None:
        self.__create_project_empresa_case = create_project_empresa_case
        self.__create_history_project_case = create_history_project_case
    
    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            body = http_request.body
            empresa_id = body['empresa_id']
            project_id = body['project_id']
            self.__create_project_empresa_case.create(
                empresa_id=empresa_id,
                project_id=project_id
            )
            self.__create_history_project_case .create(
                project_id=project_id,
                data_name="Empresa",
                description="Projeto Associado a Uma Nova Empresa"
            )
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'Project Empresa Created'
                }
            )
        except Exception as e:
            raise e from e