from src.domain.use_cases.i_delete_project_fiscal import IDeleteProjectFiscal
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.presentation.interface.controller_interface import ControllerInterface

class DeleteProjectFiscalController(ControllerInterface):

    def __init__(self, delete_project_fiscal_case:IDeleteProjectFiscal) -> None:
        self.__delete_project_fiscal_case = delete_project_fiscal_case
    
    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            body = http_request.body
            project_id = body['project_id']
            fiscal_id = body['fiscal_id']
            self.__delete_project_fiscal_case.delete(
                project_id=project_id,
                fiscal_id=fiscal_id
            )
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'Fiscal Deleted'
                }
            )
        except Exception as e:
            raise e from e