from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.presentation.interface.controller_interface import ControllerInterface
from src.domain.use_cases.i_delete_fiscal_document import IDeleteFiscalDocument

class DeleteFiscalDocumentController(ControllerInterface):

    def __init__(self, delete_fiscal_document_case:IDeleteFiscalDocument) -> None:
        self.__delete_fiscal_document_case = delete_fiscal_document_case

    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            project_id = http_request.body.get('project_id')
            fiscal_id = http_request.body.get('fiscal_id')
            document_name = http_request.body.get('document_name')

            self.__delete_fiscal_document_case.delete(
                project_id=int(project_id),
                fiscal_id=int(fiscal_id),
                document_name=document_name
            )

            return HttpResponse(
                status_code=200,
                body={"message": "Fiscal document deleted successfully"}
            )

        except Exception as e:
            raise e from e