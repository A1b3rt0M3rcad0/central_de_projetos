from src.domain.use_cases.i_create_history_project import ICreateHistoryProject
from src.domain.use_cases.i_create_project_bairro import ICreateProjectBairro
from src.domain.use_cases.i_find_bairro_by_id import IFindBairroById
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.presentation.interface.controller_interface import ControllerInterface

class CreateProjectBairroController(ControllerInterface):

    def __init__(self, 
                 create_project_bairro_case:ICreateProjectBairro, 
                 create_history_project_case:ICreateHistoryProject,
                 find_bairro_by_id:IFindBairroById
                 ) -> None:
        self.__create_project_bairro_case = create_project_bairro_case
        self.__create_history_project_case = create_history_project_case
        self.__find_bairro_by_id_case = find_bairro_by_id
    
    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            body = http_request.body
            bairro_id = body['bairro_id']
            project_id = body['project_id']
            self.__create_project_bairro_case.create(
                project_id=project_id,
                bairro_id=bairro_id
            )
            bairro = self.__find_bairro_by_id_case.find(bairro_id=bairro_id)
            self.__create_history_project_case.create(
                project_id=project_id,
                data_name='Bairro',
                description=f'Bairro: "{bairro.name}" associado'
            )
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'Bairro associado'
                }
            )
        except Exception as e:
            raise e from e