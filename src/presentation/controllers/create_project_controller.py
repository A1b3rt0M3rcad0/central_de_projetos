from src.domain.use_cases.i_create_project import ICreateProject
from src.domain.use_cases.i_create_history_project import ICreateHistoryProject
from src.domain.use_cases.i_find_project_by_name import IFindProjectByName
from src.domain.value_objects.monetary_value import MonetaryValue
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from datetime import datetime

class CreateProjectController(ControllerInterface):

    def __init__(self, 
                 create_project_case:ICreateProject, 
                 find_project_by_name_case:IFindProjectByName, 
                 create_history_project_case:ICreateHistoryProject):
        self.__create_project_case = create_project_case
        self.__find_project_by_name_case= find_project_by_name_case
        self.__create_history_project_case = create_history_project_case
    
    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            body = http_request.body
            status_id = body['status_id']
            name = body['name']
            verba_disponivel = MonetaryValue(body['verba_disponivel'])
            andamento_do_projeto = body['andamento_do_projeto']
            start_date = datetime.fromisoformat(body['start_date']) if body['start_date'] else None
            expected_completion_date = datetime.fromisoformat(body['expected_completion_date']) if body['expected_completion_date'] else None
            end_date = datetime.fromisoformat(body['end_date']) if body['end_date'] else None
            self.__create_project_case.create(
                status_id=status_id,
                name=name,
                verba_disponivel=verba_disponivel,
                andamento_do_projeto=andamento_do_projeto,
                start_date=start_date,
                expected_completion_date=expected_completion_date,
                end_date=end_date
            )
            project = self.__find_project_by_name_case.find(
                name=name
            )
            self.__create_history_project_case.create(
                project_id=project.project_id,
                data_name='Project',
                description='Projeto Inserido'
            )
            return HttpResponse(
                status_code=200,
                body = {
                    'message': 'Project Created'
                }
            )
        except Exception as e:
            raise e from e