from src.domain.use_cases.i_delete_project_type import IDeleteProjectType
from src.domain.use_cases.i_create_history_project import ICreateHistoryProject
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

class DeleteProjectTypeController(ControllerInterface):

    def __init__(self, 
                 delete_project_type_case:IDeleteProjectType,
                 create_history_project_case:ICreateHistoryProject) -> None:
        self.__delete_project_type_case = delete_project_type_case
        self.__create_history_project_case = create_history_project_case
    
    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            body = http_request.body
            project_id = body['project_id']
            types_id = body['types_id']
            
            # Deletar a associação tipo-projeto
            self.__delete_project_type_case.delete(
                project_id=project_id,
                type_id=types_id
            )
            
            # Criar histórico do projeto
            self.__create_history_project_case.create(
                project_id=project_id,
                data_name='Tipo',
                description=f'Tipo {types_id} removido do projeto'
            )
            
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'Project Type Deleted'
                }
            )
        except Exception as e:
            raise e from e