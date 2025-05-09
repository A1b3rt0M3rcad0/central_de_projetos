from src.data.use_cases.find_bairro_by_name import IFindBairroByName
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

class FindBairrobyNameController(ControllerInterface):

    def __init__(self, find_bairro_by_name_case:IFindBairroByName) -> None:
        self.__find_bairro_by_name_case = find_bairro_by_name_case
    
    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            body = http_request.body
            name = body['bairro_name']
            result = self.__find_bairro_by_name_case.find(name=name)
            return HttpResponse(
                status_code=200,
                body={
                    'messsage': 'Bairro Founded',
                    'content': {'id':result.bairro, 'name':result.name, 'created_at':result.created_at.strftime(r'%d/%m/%Y')}
                }
            )
        except Exception as e:
            raise e from e