from src.domain.use_cases.i_find_fiscal_by_name import IFindFiscalByName
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

class FindFiscalByNameController(ControllerInterface):

    def __init__(self, find_fiscal_by_name_case:IFindFiscalByName) -> None:
        self.__find_fiscal_by_name_case = find_fiscal_by_name_case
    
    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            path_params = http_request.path_params
            name = path_params['fiscal_name']
            result = self.__find_fiscal_by_name_case.find(
                name=name
            )
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'Fiscal Founded',
                    'content': {
                        'id': result.fiscal_id,
                        'name': result.name,
                        'created_at': result.created_at.strftime(r'%d/%m/%Y')
                    }
                }
            )
        except Exception as e:
            raise e from e