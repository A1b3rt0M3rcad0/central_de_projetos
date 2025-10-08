from src.domain.use_cases.i_update_fiscal_password import IUpdateFiscalPassword
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.domain.value_objects.password import Password
from src.security.hashedpassword_factory import hashedpassword_factory

class UpdateFiscalPasswordController(ControllerInterface):

    def __init__(self, 
                 update_fiscal_password_case: IUpdateFiscalPassword,
                 ) -> None:
        self.__update_fiscal_password_case = update_fiscal_password_case
    
    def handle(self, http_request: HttpRequest) -> HttpResponse:
        try:
            body = http_request.body
            name = body['name']
            password_str = body['password']
            
            # Criar Password value object e hashear usando a factory
            password = hashedpassword_factory(Password(password_str))
            
            self.__update_fiscal_password_case.update(
                name=name,
                password=password
            )
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'Fiscal password updated successfully'
                }
            )
        except Exception as e:
            raise e from e

