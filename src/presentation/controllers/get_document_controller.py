from src.domain.use_cases.i_get_document import IGetDocument
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
import mimetypes

class GetDocumentController(ControllerInterface):

    def __init__(self, get_document_case:IGetDocument) -> None:
        self.__get_document_case = get_document_case
    
    def handle(self, http_request: HttpRequest) -> HttpResponse:
        try:
            body = http_request.body
            project_id = body['project_id']
            document_name = body['document_name']

            document = self.__get_document_case.document(
                project_id=project_id,
                document_name=document_name
            )
            
            document_dict = document.to_dict()
            document_bytes = document_dict['document']

            mime_type, _ = mimetypes.guess_type(document_name)
            mime_type = mime_type or 'application/octet-stream'

            return HttpResponse(
                status_code=200,
                body=document_bytes,
                headers={
                    "Content-Type": mime_type,
                    "Content-Disposition": f'attachment; filename="{document_name}"'
                }
            )
        except Exception as e:
            raise e