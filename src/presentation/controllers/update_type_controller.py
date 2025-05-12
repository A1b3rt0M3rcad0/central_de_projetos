from src.domain.use_cases.i_update_type import IUpdateType
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.presentation.interface.controller_interface import ControllerInterface

class UpdateTypeController(ControllerInterface):

    def __init__(self, update_type_case:IUpdateType) -> None:
        self.__update_type_case = update_type_case
    
    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            body = http_request.body
            name = body['name']
            new_name = body['new_name']
            self.__update_type_case.update(
                name=name,
                new_name=new_name
            )
            return HttpResponse(
                status_code=200,
                body={
                    'message':  'type name updated'
                }
            )
        except Exception as e:
            raise e from e