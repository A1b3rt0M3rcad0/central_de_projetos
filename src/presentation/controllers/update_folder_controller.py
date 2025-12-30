from src.domain.use_cases.i_update_folder import IUpdateFolder
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.presentation.interface.controller_interface import ControllerInterface

class UpdateFolderController(ControllerInterface):

    def __init__(self, update_folder_case: IUpdateFolder) -> None:
        self.__update_folder_case = update_folder_case
    
    def handle(self, http_request: HttpRequest) -> HttpResponse:
        try:
            body = http_request.body
            folder_id = body['folder_id']
            new_name = body['new_name']
            self.__update_folder_case.update(
                folder_id=folder_id,
                new_name=new_name
            )
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'Folder updated'
                }
            )
        except Exception as e:
            raise e from e

