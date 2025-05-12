from src.domain.use_cases.i_update_bairro_from_project import IUpdateBairroFromProject
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

class UpdateBairroFromProjectController(ControllerInterface):

    def __init__(self, update_bairro_from_project_case:IUpdateBairroFromProject) -> None:
        self.__update_bairro_from_project_case = update_bairro_from_project_case
    
    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            body = http_request.body
            project_id = body['project_id']
            bairro_id = body['bairro_id']
            new_bairro_id = body['new_project_id']
            self.__update_bairro_from_project_case.update(
                project_id=project_id,
                bairro_id=bairro_id,
                new_bairro_id=new_bairro_id
            )
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'Bairro updated from projects'
                }
            )
        except Exception as e:
            raise e from e