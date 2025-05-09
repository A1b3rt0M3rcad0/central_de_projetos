from src.domain.use_cases.i_delete_type import IDeleteType
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

class DeleteTypeController(ControllerInterface):

    def __init__(self, delete_type_case:IDeleteType) -> None:
        self.__delete_type_case = delete_type_case
    
    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            body = http_request.body
            name = body['name']
            self.__delete_type_case.delete(
                name=name
            )
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'Type Deleted'
                }
            )
        except Exception as e:
            raise e from e