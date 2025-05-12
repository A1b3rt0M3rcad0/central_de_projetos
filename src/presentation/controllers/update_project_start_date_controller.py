from src.domain.use_cases.i_update_project_start_date import IUpdateProjectStartDate
from src.domain.use_cases.i_create_history_project import ICreateHistoryProject
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from datetime import datetime

class UpdateProjectStartDateController(ControllerInterface):

    def __init__(self, 
                 update_project_start_date_case:IUpdateProjectStartDate,
                 create_history_project_case:ICreateHistoryProject
                 ) -> None:
        self.__update_project_start_date_case = update_project_start_date_case
        self.__create_history_project_case = create_history_project_case
    
    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            body = http_request.body
            project_id = body['project_id']
            start_date = body['start_date']
            self.__update_project_start_date_case.update(
                project_id=project_id,
                start_date=datetime.strptime(start_date, format=r'%d/%m/%Y')
            )
            self.__create_history_project_case.create(
                project_id=project_id,
                data_name='Start Date',
                description=f'Data de inicio do projeto atualizada para {start_date}'
            )
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'Start date project updated'
                }
            )
        except Exception as e:
            raise e from e