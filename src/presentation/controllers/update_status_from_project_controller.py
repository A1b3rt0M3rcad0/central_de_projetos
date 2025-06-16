from src.domain.use_cases.i_update_status_from_project import IUpdateStatusFromProject
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

class UpdateStatusFromProjectController(ControllerInterface):

    def __init__(self, update_status_from_project:IUpdateStatusFromProject) -> None:
        self.__update_status_from_project = update_status_from_project
    
    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            body = http_request.body
            self.__update_status_from_project.update(
                project_id=body['project_id'],
                status_id=body['status_id']
            )
            return HttpResponse(
                status_code=200,
                body={
                    "message": "Project Status Updated"
                }
            )
        except Exception as e:
            raise e from e