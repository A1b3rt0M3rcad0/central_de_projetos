from src.domain.use_cases.i_create_folder import ICreateFolder
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.presentation.interface.controller_interface import ControllerInterface

class CreateFolderController(ControllerInterface):

    def __init__(self, create_folder_case: ICreateFolder) -> None:
        self.__create_folder_case = create_folder_case
    
    def handle(self, http_request: HttpRequest) -> HttpResponse:
        try:
            body = http_request.body
            name = body['name']
            self.__create_folder_case.create(
                name=name
            )
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'Folder created'
                }
            )
        except Exception as e:
            raise e from e

