from src.domain.use_cases.i_create_project_folder import ICreateProjectFolder
from src.domain.use_cases.i_create_history_project import ICreateHistoryProject
from src.domain.use_cases.i_find_folder_by_id import IFindFolderById
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.presentation.interface.controller_interface import ControllerInterface

class CreateProjectFolderController(ControllerInterface):

    def __init__(self, 
                 create_project_folder_case: ICreateProjectFolder,
                 create_history_project_case: ICreateHistoryProject,
                 find_folder_by_id: IFindFolderById
                 ) -> None:
        self.__create_project_folder_case = create_project_folder_case
        self.__create_history_project_case = create_history_project_case
        self.__find_folder_by_id_case = find_folder_by_id
    
    def handle(self, http_request: HttpRequest) -> HttpResponse:
        try:
            body = http_request.body
            project_id = body['project_id']
            folder_id = body['folder_id']
            self.__create_project_folder_case.create(
                project_id=project_id,
                folder_id=folder_id
            )
            folder = self.__find_folder_by_id_case.find(folder_id=folder_id)
            self.__create_history_project_case.create(
                project_id=project_id,
                data_name='Folder',
                description=f'Pasta: "{folder.name}" associada'
            )
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'Folder associado'
                }
            )
        except Exception as e:
            raise e from e

