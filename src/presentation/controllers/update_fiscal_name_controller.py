from src.domain.use_cases.i_update_fiscal_name import IUpdateFiscalName
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

class UpdateFiscalNameController(ControllerInterface):

    def __init__(self, 
                 update_fiscal_name_case:IUpdateFiscalName,
                 ) -> None:
        self.__update_fiscal_name_case = update_fiscal_name_case
    
    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            body = http_request.body
            name = body['name']
            new_name = body['new_name']
            self.__update_fiscal_name_case.update(
                name=name,
                new_name=new_name
            )
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'Fiscal name updated'
                }
            )
        except Exception as e:
            raise e from e