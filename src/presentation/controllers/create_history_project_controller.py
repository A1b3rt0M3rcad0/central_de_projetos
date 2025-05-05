from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.domain.use_cases.i_create_history_project import ICreateHistoryProject

class CreateHistoryProjectController(ControllerInterface):

    def __init__(self, create_history_project_case:ICreateHistoryProject) -> None:
        self.__create_history_project_case = create_history_project_case
    
    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            body = http_request.body
            project_id = body['project_id']
            data_name = body['data_name']
            description = body['description']
            self.__create_history_project_case.create(
                project_id=project_id,
                data_name=data_name,
                description=description
            )
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'History Project created'
                }
            )
        except Exception as e:
            raise e from e