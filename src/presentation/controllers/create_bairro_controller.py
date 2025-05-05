from src.domain.use_cases.i_create_bairro import ICreateBairro
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.presentation.interface.controller_interface import ControllerInterface

class CreateBairroController(ControllerInterface):

    def __init__(self, create_bairro_case:ICreateBairro) -> None:
        self.__create_bairro_case = create_bairro_case
    
    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            body = http_request.body
            bairro_name = body['bairro_name']
            self.__create_bairro_case.create(
                bairro_name
            )
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'Bairro created'
                }
            )
        except Exception as e:
            raise e from e