from src.domain.use_cases.i_find_project_bairro import IFindProjectBairro
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.presentation.interface.controller_interface import ControllerInterface

class FindProjectBairroController(ControllerInterface):

    def __init__(self, find_project_bairro_case:IFindProjectBairro) -> None:
        self.__find_project_bairro_case = find_project_bairro_case
    
    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            body = http_request.body
            project_id = body['project_id']
            bairro_id = body['bairro_id']
            result = self.__find_project_bairro_case.find(
                project_id=project_id,
                bairro_id=bairro_id
            )
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'Project Bairro Founded',
                    'content': {
                        'bairro_id': result.bairro_id,
                        'project_id': result.project_id,
                        'created_at': result.created_at.strftime(r'%d/%m/%Y')
                    }
                }
            )
        except Exception as e:
            raise e from e