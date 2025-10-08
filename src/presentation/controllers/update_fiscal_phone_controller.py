from src.domain.use_cases.i_update_fiscal_phone import IUpdateFiscalPhone
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

class UpdateFiscalPhoneController(ControllerInterface):

    def __init__(self, 
                 update_fiscal_phone_case: IUpdateFiscalPhone,
                 ) -> None:
        self.__update_fiscal_phone_case = update_fiscal_phone_case
    
    def handle(self, http_request: HttpRequest) -> HttpResponse:
        try:
            body = http_request.body
            name = body['name']
            phone = body['phone']
            self.__update_fiscal_phone_case.update(
                name=name,
                phone=phone
            )
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'Fiscal phone updated successfully'
                }
            )
        except Exception as e:
            raise e from e

