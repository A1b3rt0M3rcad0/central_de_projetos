from src.domain.use_cases.i_delete_project import IDeleteProject
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.presentation.interface.controller_interface import ControllerInterface

class DeleteProjectController(ControllerInterface):

    def __init__(self, delete_project_case:IDeleteProject) -> None:
        self.__delete_project_case = delete_project_case
    
    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            body = http_request.body
            project_id = body['project_id']
            self.__delete_project_case.delete(
                project_id=project_id
            )
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'Project Deleted'
                }
            )
        except Exception as e:
            raise e from e