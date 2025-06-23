from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.domain.use_cases.i_get_project_verba_by_bairro import IGetProjectVerbaByBairro

class GetProjectVerbaByBairroController(ControllerInterface):

    def __init__(self, get_project_verba_by_bairro:IGetProjectVerbaByBairro) -> None:
        self.__get_project_verba_by_bairro = get_project_verba_by_bairro
    
    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            result = self.__get_project_verba_by_bairro.get()
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'Verba by bairro founded',
                    'content': {
                        'verba': result['project_verba_by_bairro'],
                        'bairros': [{'id':bairro.bairro, 'name':bairro.name, 'created_at':bairro.created_at.strftime(r'%d/%m/%Y')} 
                        for bairro in result['bairros']]
                    }
                }
            )
        except Exception as e:
            raise e from e