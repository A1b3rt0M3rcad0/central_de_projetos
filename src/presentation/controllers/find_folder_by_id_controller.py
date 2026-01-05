from src.domain.use_cases.i_find_folder_by_id import IFindFolderById
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

class FindFolderByIdController(ControllerInterface):

    def __init__(self, find_folder_by_id_case: IFindFolderById) -> None:
        self.__find_folder_by_id_case = find_folder_by_id_case
    
    def handle(self, http_request: HttpRequest) -> HttpResponse:
        try:
            path_params = http_request.path_params
            folder_id = int(path_params['folder_id'])
            result = self.__find_folder_by_id_case.find(folder_id=folder_id)
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'Folder Founded',
                    'content': {
                        'id': result.folder_id,
                        'name': result.name,
                        'created_at': result.created_at.strftime(r'%d/%m/%Y') if result.created_at else None,
                        'updated_at': result.updated_at.strftime(r'%d/%m/%Y') if result.updated_at else None
                    }
                }
            )
        except Exception as e:
            raise e from e

