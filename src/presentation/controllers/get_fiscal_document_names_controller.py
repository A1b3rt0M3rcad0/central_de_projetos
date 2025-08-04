from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.presentation.interface.controller_interface import ControllerInterface
from src.domain.use_cases.i_get_fiscal_document_names import IGetFiscalDocumentNames

class GetFiscalDocumentNamesController(ControllerInterface):

    def __init__(self, get_fiscal_document_names_case:IGetFiscalDocumentNames) -> None:
        self.__get_fiscal_document_names_case = get_fiscal_document_names_case

    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            project_id = http_request.path_params.get('project_id')
            fiscal_id = http_request.path_params.get('fiscal_id')

            document_names = self.__get_fiscal_document_names_case.get_names(
                project_id=int(project_id),
                fiscal_id=int(fiscal_id)
            )

            return HttpResponse(
                status_code=200,
                body={"document_names": document_names}
            )

        except Exception as e:
            raise e from e