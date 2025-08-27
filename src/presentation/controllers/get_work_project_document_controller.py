#pylint:disable=W0612
import mimetypes
from src.domain.use_cases.i_get_work_project_document import IGetWorkProjectDocument
from src.domain.use_cases.i_get_work_project import IGetWorkProject
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

class GetWorkProjectDocumentController(ControllerInterface):
    def __init__(
        self,
        get_work_project_document_case: IGetWorkProjectDocument,
        get_work_project_case: IGetWorkProject
    ) -> None:
        self.__get_work_project_document_case = get_work_project_document_case
        self.__get_work_project_case = get_work_project_case

    def handle(self, http_request: HttpRequest) -> HttpResponse:
        try:
            path_params = http_request.path_params or {}

            work_project_id = int(path_params["work_project_id"])
            document_name = path_params["document_name"]

            # Verificar se o work_project existe
            work_project = self.__get_work_project_case.get(work_project_id=work_project_id)

            # Obter o documento
            data = self.__get_work_project_document_case.get_document(
                work_project_id=work_project_id,
                document_name=document_name
            )

            mime_type, _ = mimetypes.guess_type(document_name)
            mime_type = mime_type or "application/octet-stream"

            return HttpResponse(
                status_code=200,
                body=data,
                headers={
                    "Content-Type": mime_type,
                    "Content-Disposition": f'inline; filename="{document_name}"'
                }
            )
        except Exception as e:
            raise e from e 