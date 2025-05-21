from src.domain.use_cases.i_save_document import ISaveDocument
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.domain.value_objects.generic_document import GenericDocument


class SaveDocumentController(ControllerInterface):

    def __init__(self, save_document_use_case: ISaveDocument) -> None:
        self.__save_document_use_case = save_document_use_case

    def handle(self, http_request: HttpRequest) -> HttpResponse:
        try:
            body = http_request.body
            project_id = body['project_id']

            document = GenericDocument(
                document=body["document"],                  # bytes
                content_type=body["content_type"],          # str
                name=body["name"],                          # str (nome interno)
                document_name=body["document_name"]         # str (nome original ou exibido)
            )

            self.__save_document_use_case.save(
                document=[document],
                project_id=project_id
            )

            return HttpResponse(
                status_code=200,
                body={"message": "Document uploaded successfully"}
            )

        except Exception as e:
            raise e from e