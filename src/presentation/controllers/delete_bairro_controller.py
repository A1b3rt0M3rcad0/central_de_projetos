from src.domain.use_cases.i_delete_bairro import IDeleteBairro
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

class DeleteBairroController(ControllerInterface):

    def __init__(self, delete_bairro_case:IDeleteBairro) -> None:
        self.__delete_bairro_case = delete_bairro_case
    
    def handle(self, http_request:HttpRequest) -> HttpRequest:
        try:
            body = http_request.body
            name = body['name']
            self.__delete_bairro_case.delete(
                name=name
            )
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'Bairro Deleted'
                }
            )
        except Exception as e:
            raise e from e