#pylint:disable=W0612
from src.domain.use_cases.i_find_all_fiscal import IFindAllFiscal
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

class FindAllFiscalController(ControllerInterface):

    def __init__(self, find_all_fiscal_case:IFindAllFiscal) -> None:
        self.__find_all_fiscal_case = find_all_fiscal_case
    
    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            body = http_request.body
            result = self.__find_all_fiscal_case.find()
            return HttpResponse(
                status_code=200,
                body={
                    "message": "Fiscais Founded",
                    "content": [
                        {
                            "id": fiscal.fiscal_id,
                            "name": fiscal.name,
                            "created_at": fiscal.created_at.strftime(r'%d/%m/%Y')
                        }
                        for fiscal in result
                    ]
                }
            )
        except Exception as e:
            raise e from e