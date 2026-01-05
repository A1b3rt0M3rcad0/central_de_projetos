from src.domain.use_cases.i_find_project_folder import IFindProjectFolder
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.presentation.interface.controller_interface import ControllerInterface

class FindProjectFolderController(ControllerInterface):

    def __init__(self, find_project_folder_case: IFindProjectFolder) -> None:
        self.__find_project_folder_case = find_project_folder_case
    
    def handle(self, http_request: HttpRequest) -> HttpResponse:
        try:
            path_params = http_request.path_params
            project_id = int(path_params['project_id'])
            folder_id = int(path_params['folder_id'])
            result = self.__find_project_folder_case.find(
                project_id=project_id,
                folder_id=folder_id
            )
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'Project Folder Founded',
                    'content': {
                        'id': result.id,
                        'folder_id': result.folder_id,
                        'project_id': result.project_id,
                        'created_at': result.created_at.strftime(r'%d/%m/%Y') if result.created_at else None,
                        'updated_at': result.updated_at.strftime(r'%d/%m/%Y') if result.updated_at else None
                    }
                }
            )
        except Exception as e:
            raise e from e

