from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.presentation.interface.controller_interface import ControllerInterface
from src.domain.use_cases.i_delete_all_fiscal_documents_from_project import IDeleteAllFiscalDocumentsFromProject

class DeleteAllFiscalDocumentsFromProjectController(ControllerInterface):

    def __init__(self, delete_all_fiscal_documents_from_project_case:IDeleteAllFiscalDocumentsFromProject) -> None:
        self.__delete_all_fiscal_documents_from_project_case = delete_all_fiscal_documents_from_project_case

    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            project_id = http_request.body.get('project_id')
            fiscal_id = http_request.body.get('fiscal_id')

            self.__delete_all_fiscal_documents_from_project_case.delete_all(
                project_id=int(project_id),
                fiscal_id=int(fiscal_id)
            )

            return HttpResponse(
                status_code=200,
                body={"message": "All fiscal documents deleted successfully"}
            )

        except Exception as e:
            raise e from e