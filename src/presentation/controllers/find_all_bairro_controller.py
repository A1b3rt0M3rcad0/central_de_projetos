#pylint:disable=W0612
from src.presentation.interface.controller_interface import ControllerInterface
from src.domain.use_cases.i_find_all_bairro import IFindAllBairro
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

class FindAllBairroController(ControllerInterface):

    def __init__(self, find_all_bairro_case:IFindAllBairro) -> None:
        self.__find_all_bairro_case = find_all_bairro_case
    
    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            body = http_request.body
            result = self.__find_all_bairro_case.find()
            return HttpResponse(
                status_code=200,
                body={
                    "message": "Bairros Founded",
                    "content": [
                        {
                            "id": bairro.bairro,
                            "name": bairro.name,
                            "created_at": bairro.created_at.strftime(r'%d/%m/%Y')
                        } for bairro in result
                    ]
                }
            )
        except Exception as e:
            raise e from e