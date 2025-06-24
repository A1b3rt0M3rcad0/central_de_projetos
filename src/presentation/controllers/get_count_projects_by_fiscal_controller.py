from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.domain.use_cases.i_get_count_projects_by_fiscal import IGetCountProjectsByFiscal

class GetCountProjectsByFiscalController(ControllerInterface):

    def __init__(self, get_count_projects_by_fiscal:IGetCountProjectsByFiscal) -> None:
        self.__get_count_projects_by_fiscal = get_count_projects_by_fiscal
    
    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            result = self.__get_count_projects_by_fiscal.get()
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'Count Projects By Fiscal',
                    'content': result
                }
            )
        except Exception as e:
            raise e from e