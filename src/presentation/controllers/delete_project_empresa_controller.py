from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.domain.use_cases.i_delete_project_empresa import IDeleteProjectEmpresa
from src.domain.use_cases.i_create_history_project import ICreateHistoryProject

class DeleteProjectEmpresaController(ControllerInterface):

    def __init__(self, 
                 delete_project_empresa_case:IDeleteProjectEmpresa,
                 create_history_project_case:ICreateHistoryProject) -> None:
        self.__delete_project_empresa_case = delete_project_empresa_case
        self.__create_history_project_case = create_history_project_case
    
    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            body = http_request.body
            empresa_id = body['empresa_id']
            project_id = body['project_id']
            
            # Deletar a associação empresa-projeto
            self.__delete_project_empresa_case.delete(
                empresa_id=empresa_id,
                project_id=project_id
            )
            
            # Criar histórico do projeto
            self.__create_history_project_case.create(
                project_id=project_id,
                data_name='Empresa',
                description=f'Empresa {empresa_id} removida do projeto'
            )
            
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'Project Empresa Deleted'
                }
            )
        except Exception as e:
            raise e from e