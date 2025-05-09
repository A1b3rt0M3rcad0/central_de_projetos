from src.domain.use_cases.i_delete_status import IDeleteStatus
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

class DeleteStatusController(ControllerInterface):

    def __init__(self, delete_status_case:IDeleteStatus) -> None:
        self.__delete_status_case = delete_status_case
    
    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            body = http_request.body
            status_id = body['status_id']
            self.__delete_status_case.delete(
                status_id=status_id
            )
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'Status Deleted'
                }
            )
        except Exception as e:
            raise e from e