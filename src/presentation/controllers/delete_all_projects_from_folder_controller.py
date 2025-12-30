from src.domain.use_cases.i_delete_all_projects_from_folder import IDeleteAllProjectsFromFolder
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.presentation.interface.controller_interface import ControllerInterface

class DeleteAllProjectsFromFolderController(ControllerInterface):

    def __init__(self, delete_all_projects_from_folder_case: IDeleteAllProjectsFromFolder) -> None:
        self.__delete_all_projects_from_folder_case = delete_all_projects_from_folder_case
    
    def handle(self, http_request: HttpRequest) -> HttpResponse:
        try:
            path_params = http_request.path_params
            folder_id = int(path_params['folder_id'])
            self.__delete_all_projects_from_folder_case.delete(
                folder_id=folder_id
            )
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'All Projects From Folder Deleted'
                }
            )
        except Exception as e:
            raise e from e

