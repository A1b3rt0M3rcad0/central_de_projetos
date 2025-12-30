from src.domain.use_cases.i_delete_project_folder import IDeleteProjectFolder
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.presentation.interface.controller_interface import ControllerInterface

class DeleteProjectFolderController(ControllerInterface):

    def __init__(self, delete_project_folder_case: IDeleteProjectFolder) -> None:
        self.__delete_project_folder_case = delete_project_folder_case
    
    def handle(self, http_request: HttpRequest) -> HttpResponse:
        try:
            body = http_request.body
            project_id = body['project_id']
            folder_id = body['folder_id']
            self.__delete_project_folder_case.delete(
                project_id=project_id,
                folder_id=folder_id
            )
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'Project Folder Deleted'
                }
            )
        except Exception as e:
            raise e from e

