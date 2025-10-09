from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.domain.use_cases.i_update_fiscal_status import IUpdateFiscalStatus
from src.presentation.interface.controller_interface import ControllerInterface

class UpdateFiscalStatusController(ControllerInterface):

    def __init__(self, update_fiscal_status_case: IUpdateFiscalStatus) -> None:
        self.__update_fiscal_status_case = update_fiscal_status_case

    def handle(self, http_request: HttpRequest) -> HttpResponse:
        fiscal_id = http_request.path_params['fiscal_id']
        body = http_request.body
        is_active = body['is_active']

        self.__update_fiscal_status_case.update(
            fiscal_id=fiscal_id,
            is_active=is_active
        )

        return HttpResponse(
            status_code=200,
            body={
                'message': 'Fiscal status updated successfully',
                'fiscal_id': fiscal_id,
                'is_active': is_active
            }
        )

