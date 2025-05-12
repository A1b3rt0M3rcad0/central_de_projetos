from src.domain.use_cases.i_update_bairro_name import IUpdateBairroName
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.presentation.interface.controller_interface import ControllerInterface

class UpdateBairroNameController(ControllerInterface):

    def __init__(self, update_bairro_name_case:IUpdateBairroName) -> None:
        self.__update_bairro_name_case = update_bairro_name_case
    
    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            body = http_request.body
            name = body['name']
            new_name = body['new_name']
            self.__update_bairro_name_case.update(
                name=name,
                new_name=new_name
            )
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'Name from bairro updated'
                }
            )
        except Exception as e:
            raise e from e