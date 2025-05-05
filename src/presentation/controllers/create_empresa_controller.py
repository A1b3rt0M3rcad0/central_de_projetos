from src.domain.use_cases.i_create_empresa import ICreateEmpresa
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

class CreateEmpresaController(ControllerInterface):

    def __init__(self, create_empresa_case:ICreateEmpresa) -> None:
        self.__create_empresa_case = create_empresa_case
    
    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            body = http_request.body
            empresa_name = body['empresa_name']
            self.__create_empresa_case.create(
                name=empresa_name
            )
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'Empresa created'
                }
            )
        except Exception as e:
            raise e from e