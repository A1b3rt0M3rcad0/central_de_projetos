from src.domain.use_cases.i_create_project_type import ICreateProjectType
from src.domain.use_cases.i_create_history_project import ICreateHistoryProject
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

class CreateProjectTypeController(ControllerInterface):

    def __init__(self, 
                 create_project_type_case:ICreateProjectType,
                 create_history_project_case:ICreateHistoryProject) -> None:
        self.__create_project_type_case = create_project_type_case
        self.__create_history_project_case = create_history_project_case
    
    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            body = http_request.body
            project_id = body['project_id']
            type_id = body['types_id']
            self.__create_project_type_case.create(
                project_id=project_id,
                type_id=type_id
            )
            
            # Criar histórico do projeto
            self.__create_history_project_case.create(
                project_id=project_id,
                data_name='Tipo de Projeto',
                description=f'Tipo de projeto {type_id} associado ao projeto'
            )
            
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'Project Type Created'
                }
            )
        except Exception as e:
            raise e from e