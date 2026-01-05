from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.domain.use_cases.i_count_folders import ICountFolders

class CountFoldersController(ControllerInterface):

    def __init__(self, count_folders: ICountFolders) -> None:
        self.__count_folders = count_folders
    
    def handle(self, http_request: HttpRequest) -> HttpResponse:
        try:
            query_params = http_request.query_params
            search_term = query_params.get('search')
            count = self.__count_folders.count(search_term=search_term)
            return HttpResponse(
                status_code=200,
                body={
                    'message': "Count Folders",
                    'content': count
                }
            )
        except Exception as e:
            raise e from e

