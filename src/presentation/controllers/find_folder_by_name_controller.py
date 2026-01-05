from src.domain.use_cases.i_find_folder_by_name import IFindFolderByName
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

class FindFolderByNameController(ControllerInterface):

    def __init__(self, find_folder_by_name_case: IFindFolderByName) -> None:
        self.__find_folder_by_name_case = find_folder_by_name_case
    
    def handle(self, http_request: HttpRequest) -> HttpResponse:
        try:
            path_params = http_request.path_params
            name = path_params['folder_name']
            result = self.__find_folder_by_name_case.find(name=name)
            if result is None:
                return HttpResponse(
                    status_code=404,
                    body={
                        'message': 'Folder not found'
                    }
                )
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

