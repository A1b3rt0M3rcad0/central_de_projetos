from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.domain.use_cases.i_login_fiscal import ILoginFiscal
from src.domain.use_cases.i_create_refresh_token_fiscal import ICreateRefreshTokenFiscal
from src.domain.use_cases.i_update_refresh_token_fiscal import IUpdateRefreshTokenFiscal
from src.domain.value_objects.password import Password
from src.domain.value_objects.email import Email
from src.presentation.interface.controller_interface import ControllerInterface


class LoginFiscalController(ControllerInterface):

    def __init__(self, 
                 login_fiscal_case: ILoginFiscal,
                 create_refresh_token_fiscal: ICreateRefreshTokenFiscal,
                 update_refresh_token_fiscal: IUpdateRefreshTokenFiscal
                 ) -> None:
        self.__login_fiscal_case = login_fiscal_case
        self.__create_refresh_token_fiscal = create_refresh_token_fiscal
        self.__update_refresh_token_fiscal = update_refresh_token_fiscal
    
    def handle(self, http_request: HttpRequest) -> HttpResponse:
        body = http_request.body
        email = Email(body['email'])
        password = Password(body['password'])
        token = self.__login_fiscal_case.check(
            email=email,
            password=password
        )
        self._create_refresh_token_fiscal(email=email)
        return HttpResponse(
            status_code=200,
            body={
                'token': token
            }
        )
    
    def _create_refresh_token_fiscal(self, email: Email) -> None:
        try:
            self.__create_refresh_token_fiscal.create(
                email=email
            )
        except (ValueError, TypeError, AttributeError):
            # If there's any error creating the refresh token, we'll try to update it
            try:
                self.__update_refresh_token_fiscal.update(
                    fiscal_email=email,
                    new_token=self.__create_refresh_token_fiscal.generate_token(email)
                )
            except (ValueError, TypeError, AttributeError) as update_error:
                # If both create and update fail, we'll just log the error but not fail the login
                # This ensures that login still works even if refresh token operations fail
                print(f"Warning: Failed to create/update refresh token for fiscal {email.email}: {update_error}") 