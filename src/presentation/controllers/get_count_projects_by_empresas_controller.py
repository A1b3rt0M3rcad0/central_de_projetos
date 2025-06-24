from src.domain.use_cases.i_get_count_projects_by_empresas import IGetCountProjectsByEmpresas
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

class GetCountProjectsByEmpresasController(ControllerInterface):

    def __init__(self, get_count_projects_by_empresas:IGetCountProjectsByEmpresas) -> None:
        self.__get_count_projects_by_empresas = get_count_projects_by_empresas
    
    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'Count Projects By Empresas',
                    'content': self.__get_count_projects_by_empresas.get()
                }
            )
        except Exception as e:
            raise e from e