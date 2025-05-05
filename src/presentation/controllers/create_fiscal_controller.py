from src.domain.use_cases.i_create_fiscal import ICreateFiscal
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

class CreateFiscalController(ControllerInterface):

    def __init__(self, create_fiscal_case:ICreateFiscal) -> None:
        self.__create_fiscal_case = create_fiscal_case
    
    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            body = http_request.body
            fiscal_name = body['fiscal_name']
            self.__create_fiscal_case.create(
                name=fiscal_name
            )
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'Fiscal created'
                }
            )
        except Exception as e:
            raise e from e