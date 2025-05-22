#pylint:disable=W0612
from src.domain.use_cases.i_find_all_types import IFindAllTypes
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

class FindAllTypesController(ControllerInterface):

    def __init__(self, find_all_types_case:IFindAllTypes) -> None:
        self.__find_all_types_case = find_all_types_case
    
    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            body = http_request.body
            results = self.__find_all_types_case.find()
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'Types Founded',
                    'content': [
                        {
                            'id': types.types_id,
                            'name': types.name,
                            'created_at': types.created_at
                        }
                        for types in results
                    ]
                }
            )
        except Exception as e:
            raise e from e