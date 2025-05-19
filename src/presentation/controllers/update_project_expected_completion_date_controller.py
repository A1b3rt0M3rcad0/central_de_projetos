from src.domain.use_cases.i_update_project_expected_completion_date_entry import IUpdateProjectExpectedCompletionDate
from src.domain.use_cases.i_create_history_project import ICreateHistoryProject
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from datetime import datetime

class UpdateProjectExpectedCompletionDateController(ControllerInterface):

    def __init__(self, 
                update_project_expected_completion_date_case:IUpdateProjectExpectedCompletionDate,
                create_history_project_case:ICreateHistoryProject 
                ) -> None:
        self.__update_project_expected_completion_date_case = update_project_expected_completion_date_case
        self.__create_history_project_case= create_history_project_case
    
    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            body = http_request.body
            project_id = body['project_id']
            expected_completion_date = body['expected_completion_date']
            self.__update_project_expected_completion_date_case.update(
                project_id=project_id,
                expected_completion_date=datetime.fromisoformat(expected_completion_date)
            )
            self.__create_history_project_case.create(
                project_id=project_id,
                data_name='Data de finalização esperada',
                description=f'Data de finalização esperada atualizada para {expected_completion_date}'
            )
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'Expected Completion Date Updated'
                }
            )
        except Exception as e:
            raise e from e