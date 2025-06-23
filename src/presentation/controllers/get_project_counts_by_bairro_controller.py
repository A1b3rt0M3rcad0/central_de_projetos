from src.domain.use_cases.i_get_project_counts_by_bairro import IGetProjectCountsByBairro
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

class GetProjectCountsByBairroController(ControllerInterface):

    def __init__(self, get_project_counts_by_bairro:IGetProjectCountsByBairro) -> None:
        self.__get_project_counts_by_bairro = get_project_counts_by_bairro
    
    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            result = self.__get_project_counts_by_bairro.get()
            bairros = [
                {
                    'id': bairro.bairro,
                    'name': bairro.name,
                    'created_at': bairro.created_at.strftime(r'%d/%m/%Y')
                }

                for bairro in result['bairros']
            ]
            project_bairro = result['projectBairro']
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'Counts project per bairro founded',
                    'content': {
                        'bairros': bairros,
                        'counts': project_bairro
                    }
                }
            )
        except Exception as e:
            raise e from e