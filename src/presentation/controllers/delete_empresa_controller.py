from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.domain.use_cases.i_delete_empresa import IDeleteEmpresa


class DeleteEmpresaController(ControllerInterface):

    def __init__(self, delete_empresa_case:IDeleteEmpresa) -> None:
        self.__delete_empresa_case = delete_empresa_case
    
    def handle(self, http_request:HttpRequest) -> HttpRequest:
        try:
            body = http_request.body
            name = body['name']
            self.__delete_empresa_case.delete(
                name=name
            )
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'Empresa Deleted'
                }
            )
        except Exception as e:
            raise e from e