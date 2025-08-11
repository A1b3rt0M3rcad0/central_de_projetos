from src.domain.use_cases.i_delete_project_bairro import IDeleteProjectBairro
from src.domain.use_cases.i_create_history_project import ICreateHistoryProject
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.presentation.interface.controller_interface import ControllerInterface

class DeleteProjectBairroController(ControllerInterface):

    def __init__(self, 
                 delete_project_bairro_case:IDeleteProjectBairro,
                 create_history_project_case:ICreateHistoryProject) -> None:
        self.__delete_project_bairro_case = delete_project_bairro_case
        self.__create_history_project_case = create_history_project_case
    
    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            body = http_request.body
            project_id = body['project_id']
            bairro_id = body['bairro_id']
            
            # Deletar a associação bairro-projeto
            self.__delete_project_bairro_case.delete(
                project_id=project_id,
                bairro_id=bairro_id
            )
            
            # Criar histórico do projeto
            self.__create_history_project_case.create(
                project_id=project_id,
                data_name='Bairro',
                description=f'Bairro {bairro_id} removido do projeto'
            )
            
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'ProjectBairro Deleted'
                }
            )
        except Exception as e:
            raise e from e