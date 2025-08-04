from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.presentation.interface.controller_interface import ControllerInterface
from src.domain.use_cases.i_get_fiscal_document import IGetFiscalDocument

class ViewFiscalDocumentController(ControllerInterface):

    def __init__(self, get_fiscal_document_case:IGetFiscalDocument) -> None:
        self.__get_fiscal_document_case = get_fiscal_document_case

    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            project_id = http_request.path_params.get('project_id')
            fiscal_id = http_request.path_params.get('fiscal_id')
            document_name = http_request.path_params.get('document_name')

            document = self.__get_fiscal_document_case.get(
                project_id=int(project_id),
                fiscal_id=int(fiscal_id),
                document_name=document_name
            )

            return HttpResponse(
                status_code=200,
                body=document.value(),
                headers={
                    "Content-Type": document.content_type
                }
            )

        except Exception as e:
            raise e from e 