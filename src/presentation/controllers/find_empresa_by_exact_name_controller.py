from src.domain.use_cases.i_find_empresa_by_exact_name import IFindEmpresaByExactName
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.presentation.interface.controller_interface import ControllerInterface

class FindEmpresaByExactNameController(ControllerInterface):

    def __init__(self, find_empresa_by_exact_name_case:IFindEmpresaByExactName) -> None:
        self.__find_empresa_by_exact_name_case = find_empresa_by_exact_name_case
    
    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            body = http_request.body
            name = body['empresa_name']
            result = self.__find_empresa_by_exact_name_case.find(
                name=name
            )
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'Empresa Founded',
                    'content': {
                        'id': result.empresa_id,
                        'name': result.name,
                        'created_at': result.created_at
                    }
                }
            )
        except Exception as e:
            raise e from e