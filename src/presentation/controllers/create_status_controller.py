from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.presentation.interface.controller_interface import ControllerInterface
from src.domain.use_cases.i_create_status import ICreateStatus

class CreateStatusController(ControllerInterface):

    def __init__(self, create_status_case:ICreateStatus) -> None:
        self.__create_status_case = create_status_case
    
    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            body = http_request.body
            description = body['description']
            self.__create_status_case.create(
                description=description
            )
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'Status Created'
                }
            )
        except Exception as e:
            raise e from e