from src.domain.use_cases.i_delete_document import IDeleteDocument
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

class DeleteDocumentController(ControllerInterface):

    def __init__(self, delete_document_case:IDeleteDocument) -> None:
        self.__delete_document_case = delete_document_case
    
    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            body = http_request.body
            project_id = body['project_id']
            document_name = body['document_name']
            self.__delete_document_case.delete(
                project_id=project_id,
                document_name=document_name
            )
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'Document Deleted'
                }
            )
        except Exception as e:
            raise e from e