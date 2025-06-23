from src.domain.use_cases.i_get_project_status_count_by_bairro import IGetProjectStatusCountByBairro
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

class GetProjectStatusCountByBairroController(ControllerInterface):

    def __init__(self, get_project_status_caount_by_bairro:IGetProjectStatusCountByBairro) -> None:
        self.__get_project_status_count_by_bairro = get_project_status_caount_by_bairro
    
    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            result = self.__get_project_status_count_by_bairro.get()
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'Project Status from Bairro founded',
                    'content': {
                        'bairros': [
                            {
                                'id':bairro.bairro,
                                'name':bairro.name,
                                'created_at':bairro.created_at.strftime(r'%d/%m/%Y'),
                            }
                            for bairro in result['bairros']
                        ],
                        'status': result['project_status_by_bairro']
                    }
                }
            )
        except Exception as e:
            raise e from e