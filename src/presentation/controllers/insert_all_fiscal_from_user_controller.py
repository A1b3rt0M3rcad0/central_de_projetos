from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.domain.use_cases.i_insert_all_fiscal_from_user import IInsertAllFiscalFromFiscalUseCase
from src.domain.value_objects.email import Email
from src.domain.value_objects.password import Password
from src.security.hashedpassword_factory import hashedpassword_factory

class InsertAllFiscalFromFiscalController(ControllerInterface):
    def __init__(self, use_case: IInsertAllFiscalFromFiscalUseCase):
        self.use_case = use_case

    def handle(self, http_request: HttpRequest) -> HttpResponse:
        try:
            body = http_request.body or {}
            name = body["name"]
            email = Email(body["email"])
            password = hashedpassword_factory(Password(body["password"]))
            phone = body["phone"]
            self.use_case.execute(name, email, password, phone)
            return HttpResponse(status_code=201, body={"message": "Fiscal inserted successfully"})
        except Exception as e:
            raise e from e
