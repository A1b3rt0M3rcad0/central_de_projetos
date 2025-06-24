from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.domain.use_cases.i_count_fiscals import ICountFiscals

class CountFiscalsController(ControllerInterface):

    def __init__(self, count_fiscals:ICountFiscals) -> None:
        self.__count_fiscals = count_fiscals
    
    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'Count Fiscals',
                    'content': self.__count_fiscals.count()
                }
            )
        except Exception as e:
            raise e from e