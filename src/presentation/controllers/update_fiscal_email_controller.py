from src.domain.use_cases.i_update_fiscal_email import IUpdateFiscalEmail
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.domain.value_objects.email import Email

class UpdateFiscalEmailController(ControllerInterface):

    def __init__(self, 
                 update_fiscal_email_case: IUpdateFiscalEmail,
                 ) -> None:
        self.__update_fiscal_email_case = update_fiscal_email_case
    
    def handle(self, http_request: HttpRequest) -> HttpResponse:
        try:
            body = http_request.body
            name = body['name']
            email = Email(body['email'])
            self.__update_fiscal_email_case.update(
                name=name,
                email=email
            )
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'Fiscal email updated successfully'
                }
            )
        except Exception as e:
            raise e from e

