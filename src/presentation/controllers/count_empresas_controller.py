from src.domain.use_cases.i_count_empresas import ICountEmpresas
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

class CountEmpresasController(ControllerInterface):
    
    def __init__(self, count_empresas:ICountEmpresas) -> None:
        self.__count_empresas = count_empresas
    
    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'Count Empresas',
                    'content': self.__count_empresas.count()
                }
            )
        except Exception as e:
            raise e from e