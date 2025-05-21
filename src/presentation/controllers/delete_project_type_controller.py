from src.domain.use_cases.i_delete_project_type import IDeleteProjectType
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

class DeleteProjectTypeController(ControllerInterface):

    def __init__(self, delete_project_type_case:IDeleteProjectType) -> None:
        self.__delete_project_type_case = delete_project_type_case
    
    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            body = http_request.body
            project_id = body['project_id']
            types_id = body['types_id']
            self.__delete_project_type_case.delete(
                project_id=project_id,
                type_id=types_id
            )
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'Project Type Deleted'
                }
            )
        except Exception as e:
            raise e from e