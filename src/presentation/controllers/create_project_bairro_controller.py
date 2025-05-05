#pylint:disable=all
from src.domain.use_cases.i_create_history_project import ICreateHistoryProject
from src.domain.use_cases.i_create_project_bairro import ICreateProjectBairro
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.presentation.interface.controller_interface import ControllerInterface

class CreateProjectBairroController(ControllerInterface):

    def __init__(self, create_project_bairro_case:ICreateProjectBairro, create_history_project_case:ICreateHistoryProject) -> None:
        self.__create_project_bairro_case = create_project_bairro_case
        self.__create_history_project_case = create_history_project_case
    
    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            body = http_request.body
            bairro_id = body['bairro_id']
            project_id = body['project_id']
            self.__create_project_bairro_case.create(
                project_id=project_id,
                bairro_id=bairro_id
            )

        except Exception as e:
            raise e from e