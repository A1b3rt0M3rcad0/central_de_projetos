from src.domain.use_cases.i_update_empresa import IUpdateEmpresa
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.presentation.interface.controller_interface import ControllerInterface

class UpdateEmpresaController(ControllerInterface):

    def __init__(self, update_empresa_case:IUpdateEmpresa) -> None:
        self.__update_empresa_case = update_empresa_case
    
    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            body = http_request.body
            name = body['name']
            new_name = body['new_name']
            self.__update_empresa_case.update(
                name=name,
                new_name=new_name
            )
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'Empresa Updated'
                }
            )
        except Exception as e:
            raise e from e