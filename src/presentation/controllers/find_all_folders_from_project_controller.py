from src.domain.use_cases.i_find_all_folders_from_project import IFindAllFoldersFromProject
from src.domain.use_cases.i_find_folder_by_id import IFindFolderById
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

class FindAllFoldersFromProjectController(ControllerInterface):

    def __init__(self, find_all_folders_from_project_case: IFindAllFoldersFromProject, find_folder_by_id: IFindFolderById) -> None:
        self.__find_all_folders_from_project_case = find_all_folders_from_project_case
        self.__find_folder_by_id_case = find_folder_by_id
    
    def handle(self, http_request: HttpRequest) -> HttpResponse:
        try:
            path_params = http_request.path_params
            project_id = int(path_params['project_id'])
            project_folder_results = self.__find_all_folders_from_project_case.find(project_id=project_id)
            folders = [self.__find_folder_by_id_case.find(folder_id=project_folder.folder_id)
                      for project_folder in project_folder_results
                      ]
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'Folders Founded',
                    'content': [
                        {
                            'id': folder.folder_id,
                            'name': folder.name,
                            'created_at': folder.created_at.strftime(r'%d/%m/%Y') if folder.created_at else None,
                            'updated_at': folder.updated_at.strftime(r'%d/%m/%Y') if folder.updated_at else None
                        }
                        for folder in folders
                    ]
                }
            )
        except Exception as e:
            raise e from e

