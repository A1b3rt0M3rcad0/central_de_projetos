from src.domain.use_cases.i_delete_work_project import IDeleteWorkProject
from src.domain.use_cases.i_create_history_project import ICreateHistoryProject
from src.domain.use_cases.i_get_work_project import IGetWorkProject
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

class DeleteWorkProjectController(ControllerInterface):

    def __init__(self, 
                 delete_work_project_case:IDeleteWorkProject,
                 create_history_project_case:ICreateHistoryProject,
                 get_work_project_case:IGetWorkProject) -> None:
        self.__delete_work_project_case = delete_work_project_case
        self.__create_history_project_case = create_history_project_case
        self.__get_work_project_case = get_work_project_case
    
    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            path_params = http_request.path_params
            work_project_id = int(path_params['work_project_id'])
            
            # Obter informações do work project antes de deletar para o histórico
            work_project = self.__get_work_project_case.get(work_project_id=work_project_id)
            
            # Deletar o work project
            self.__delete_work_project_case.delete(work_project_id=work_project_id)
            
            # Criar histórico do projeto
            self.__create_history_project_case.create(
                project_id=work_project.project_id,
                data_name='Work Project',
                description=f'Work project "{work_project.title}" deletado'
            )
            
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'Work Project deleted successfully',
                    'work_project_id': work_project_id
                }
            )
        except Exception as e:
            raise e from e 