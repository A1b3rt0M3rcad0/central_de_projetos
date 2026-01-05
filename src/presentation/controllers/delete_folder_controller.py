from src.domain.use_cases.i_delete_folder import IDeleteFolder
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

class DeleteFolderController(ControllerInterface):

    def __init__(self, delete_folder_case: IDeleteFolder) -> None:
        self.__delete_folder_case = delete_folder_case
    
    def handle(self, http_request: HttpRequest) -> HttpResponse:
        try:
            body = http_request.body
            folder_id = body['folder_id']
            self.__delete_folder_case.delete(
                folder_id=folder_id
            )
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'Folder Deleted'
                }
            )
        except Exception as e:
            raise e from e

