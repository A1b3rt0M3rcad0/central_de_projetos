#pylint:disable=W0612
from src.presentation.interface.controller_interface import ControllerInterface
from src.domain.use_cases.i_find_all_folder import IFindAllFolder
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

class FindAllFolderController(ControllerInterface):

    def __init__(self, find_all_folder_case: IFindAllFolder) -> None:
        self.__find_all_folder_case = find_all_folder_case
    
    def handle(self, http_request: HttpRequest) -> HttpResponse:
        try:
            result = self.__find_all_folder_case.find()
            return HttpResponse(
                status_code=200,
                body={
                    "message": "Folders Founded",
                    "content": [
                        {
                            "id": folder.folder_id,
                            "name": folder.name,
                            "created_at": folder.created_at.strftime(r'%d/%m/%Y') if folder.created_at else None,
                            "updated_at": folder.updated_at.strftime(r'%d/%m/%Y') if folder.updated_at else None
                        } for folder in result
                    ]
                }
            )
        except Exception as e:
            raise e from e

