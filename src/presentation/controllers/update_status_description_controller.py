from src.domain.use_cases.i_update_status_description import IUpdateStatusDescription
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

class UpdateStatusDescriptionController(ControllerInterface):

    def __init__(self, update_status_description_case:IUpdateStatusDescription) -> None:
        self.__update_status_description_case = update_status_description_case
    
    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            body = http_request.body
            description = body['description']
            self.__update_status_description_case.update(
                description=description
            )
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'status description updated'
                }
            )
        except Exception as e:
            raise e from e