from src.domain.use_cases.i_update_project_end_date import IUpdateProjectEndDate
from src.domain.use_cases.i_create_history_project import ICreateHistoryProject
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from datetime import datetime

class UpdateProjectEndDateController(ControllerInterface):

    def __init__(self,
                update_project_end_date_case:IUpdateProjectEndDate,
                create_history_project_case:ICreateHistoryProject
                ) -> None:
        self.__update_project_end_date_case = update_project_end_date_case
        self.__create_history_project_case = create_history_project_case
    
    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            body = http_request.body
            project_id = body['project_id']
            end_date = body['end_date']
            self.__update_project_end_date_case.update(
                project_id=project_id,
                end_date=datetime.strptime(end_date, format=r'%d/%m/%Y')
            )
            self.__create_history_project_case.create(
                project_id=project_id,
                data_name='End Date',
                description=f'Data de finalização trocada para {end_date}'
            )
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'end_date updated'
                }
            )
        except Exception as e:
            raise e from e