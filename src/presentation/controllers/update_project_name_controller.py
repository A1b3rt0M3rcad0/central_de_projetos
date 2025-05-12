from src.domain.use_cases.i_update_project_name import IUpdateProjectName
from src.domain.use_cases.i_create_history_project import ICreateHistoryProject
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

class UpdateProjectNameController(ControllerInterface):

    def __init__(self, 
                 update_project_name_case:IUpdateProjectName,
                 create_history_project_case:ICreateHistoryProject
                 ) -> None:
        self.__update_project_name_case = update_project_name_case
        self.__create_history_project_case = create_history_project_case
    
    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            body = http_request.body
            project_id = body['project_id']
            name = body['name']
            self.__update_project_name_case.update(
                project_id=project_id,
                name=name
            )
            self.__create_history_project_case.create(
                project_id=project_id,
                data_name='Nome',
                description=f'Nome do projeto atualizado para {name}'
            )
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'project name updated'
                }
            )
        except Exception as e:
            raise e from e