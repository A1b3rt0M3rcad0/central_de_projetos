from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.domain.use_cases.i_count_bairros import ICountBairros

class CountBairrosController(ControllerInterface):

    def __init__(self, count_bairros:ICountBairros) -> None:
        self.__count_bairros = count_bairros
    
    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            return HttpResponse(
                status_code=200,
                body={
                    'message': "Count Bairros",
                    'content': self.__count_bairros.count()
                }
            )
        except Exception as e:
            raise e from e