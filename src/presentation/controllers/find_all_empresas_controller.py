#pylint:disable=W0612
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.domain.use_cases.i_find_all_empresas import IFindAllEmpresas

class FindAllEmpresasController(ControllerInterface):

    def __init__(self, find_all_empresas_case:IFindAllEmpresas) -> None:
        self.__find_all_empresas_case = find_all_empresas_case
    
    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            body = http_request.body
            result = self.__find_all_empresas_case.find()
            response = [
                {
                    "id": empresa.empresa_id,
                    "name": empresa.name,
                    "created_at": empresa.created_at.strftime(r'%d/%m/%Y')
                }
                for empresa in result
            ]
            return HttpResponse(
                status_code=200,
                body={
                    "message": "Empresas Founded",
                    "content": response
                }
            )
        except Exception as e:
            raise e from e