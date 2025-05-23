from src.domain.use_cases.i_create_type import ICreateType
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.presentation.interface.controller_interface import ControllerInterface

class CreateTypeController(ControllerInterface):

    def __init__(self, create_type_case:ICreateType) -> None:
        self.__create_type_case = create_type_case
    
    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            body = http_request.body
            name = body['name']
            self.__create_type_case.create(
                name=name
            )
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'Type Created'
                }
            )
        except Exception as e:
            raise e from e