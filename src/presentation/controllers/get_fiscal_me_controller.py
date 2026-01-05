from src.domain.use_cases.i_find_fiscal_by_id import IFindFiscalById
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.presentation.interface.controller_interface import ControllerInterface


class GetFiscalMeController(ControllerInterface):

    def __init__(self, find_fiscal_by_id_case: IFindFiscalById) -> None:
        self.__find_fiscal_by_id_case = find_fiscal_by_id_case

    def handle(self, http_request: HttpRequest) -> HttpResponse:
        try:
            body = http_request.body or {}
            fiscal_id = int(body.get('fiscal_id'))

            fiscal = self.__find_fiscal_by_id_case.find(fiscal_id=fiscal_id)

            return HttpResponse(
                status_code=200,
                body={
                    'message': 'Fiscal Founded',
                    'content': {
                        'id': fiscal.fiscal_id,
                        'name': fiscal.name,
                        'email': getattr(fiscal, 'email', None),
                        'phone': getattr(fiscal, 'phone', None),
                        'created_at': fiscal.created_at.strftime(r'%d/%m/%Y') if fiscal.created_at else None
                    }
                }
            )
        except Exception as e:
            raise e from e


