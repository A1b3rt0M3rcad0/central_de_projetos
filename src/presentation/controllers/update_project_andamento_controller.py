from src.domain.use_cases.i_update_project_andamento import IUpdateProjectAndamento
from src.domain.use_cases.i_create_history_project import ICreateHistoryProject
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

class UpdateProjectAndamentoController(ControllerInterface):

    def __init__(self, 
                 update_project_andamento_case:IUpdateProjectAndamento,
                 create_history_project_case:ICreateHistoryProject
                 ) -> None:
        self.__update_project_andamento_case = update_project_andamento_case
        self.__create_history_project_case = create_history_project_case
    
    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            body = http_request.body
            project_id = body['project_id']
            andamento_do_projeto = body['andamento_do_projeto']
            self.__update_project_andamento_case.update(
                project_id=project_id,
                andamento_do_projeto=andamento_do_projeto
            )
            self.__create_history_project_case.create(
                project_id=project_id,
                data_name='Andamento do Projeto',
                description=f'Andamento do projeto atualizado para {andamento_do_projeto}'
            )
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'andamento_do_projeto updated'
                }
            )
        except Exception as e:
            raise e from e