from src.domain.use_cases.i_get_project_types_count_by_bairro import IGetProjectTypesCountByBairro
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

class GetProjectTypesCountByBairroController(ControllerInterface):

    def __init__(self, get_project_types_count_by_bairro:IGetProjectTypesCountByBairro) -> None:
        self.__get_project_types_count_by_bairro = get_project_types_count_by_bairro
    
    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            result = self.__get_project_types_count_by_bairro.get()
            types = [
                {
                    'id': types_model.types_id,
                    'name': types_model.name,
                    'created_at': types_model.created_at.strftime(r'%d/%m/%Y')
                }
                for types_model in result['types']
            ]
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'count types by bairro founded',
                    'content': {
                        'types': types,
                        'types_count_by_bairro': result['types_count_by_bairro']
                    }
                }
            )
        except Exception as e:
            raise e from e