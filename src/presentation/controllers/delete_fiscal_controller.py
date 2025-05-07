from src.domain.use_cases.i_delete_fiscal import IDeleteFiscal
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

class DeleteFiscalController(ControllerInterface):

    def __init__(self, delete_fiscal_case:IDeleteFiscal) -> None:
        self.__delete_fiscal_case = delete_fiscal_case
    
    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            body = http_request.body
            name = body['name']
            self.__delete_fiscal_case.delete(
                name = name
            )
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'Fiscal Deleted'
                }
            )
        except Exception as e:
            raise e from e