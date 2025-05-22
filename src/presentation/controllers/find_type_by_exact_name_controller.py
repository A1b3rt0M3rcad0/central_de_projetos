from src.domain.use_cases.i_find_type_by_exact_name import IFindTypeByExactName
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.presentation.interface.controller_interface import ControllerInterface

class FindTypeByExactNameController(ControllerInterface):

    def __init__(self, find_type_by_exact_name_case:IFindTypeByExactName) -> None:
        self.__find_type_by_exact_name_case = find_type_by_exact_name_case
    
    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            path_params = http_request.path_params
            name = path_params['type_name']
            result = self.__find_type_by_exact_name_case.find(
                name=name
            )
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'Type Founded',
                    'content': {
                        'id': result.types_id,
                        'name': result.name,
                        'created_at:': result.created_at.strftime(r'%d/%m/%Y')
                    }
                }
            )
        except Exception as e:
            raise e from e