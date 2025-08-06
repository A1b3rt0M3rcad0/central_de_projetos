from src.domain.use_cases.i_update_status_from_project import IUpdateStatusFromProject
from src.domain.use_cases.i_create_history_project import ICreateHistoryProject
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

class UpdateStatusFromProjectController(ControllerInterface):

    def __init__(self, 
                 update_status_from_project:IUpdateStatusFromProject,
                 create_history_project_case:ICreateHistoryProject) -> None:
        self.__update_status_from_project = update_status_from_project
        self.__create_history_project_case = create_history_project_case
    
    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            body = http_request.body
            project_id = body['project_id']
            status_id = body['status_id']
            
            self.__update_status_from_project.update(
                project_id=project_id,
                status_id=status_id
            )
            
            # Criar histórico do projeto
            self.__create_history_project_case.create(
                project_id=project_id,
                data_name='Status',
                description=f'Status do projeto atualizado para ID: {status_id}'
            )
            
            return HttpResponse(
                status_code=200,
                body={
                    "message": "Project Status Updated"
                }
            )
        except Exception as e:
            raise e from e