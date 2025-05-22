from src.domain.use_cases.i_delete_all_documents_from_project import IDeleteAllDocumentsFromProject
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

class DeleteAllDocumentsFromProjectController(ControllerInterface):

    def __init__(self, delete_all_documents_from_project_case:IDeleteAllDocumentsFromProject) -> None:
        self.__delete_all_documents_from_project_case = delete_all_documents_from_project_case
    
    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            body = http_request.body
            project_id = body['project_id']
            self.__delete_all_documents_from_project_case.delete(
                project_id=project_id
            )
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'All Documents from project deleted'
                }
            )
        except Exception as e:
            raise e from e