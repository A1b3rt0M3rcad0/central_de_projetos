import mimetypes
from src.domain.use_cases.i_get_work_project_document import IGetWorkProjectDocument
from src.domain.use_cases.i_get_work_project import IGetWorkProject
from src.domain.use_cases.i_find_project_fiscal import IFindProjectFiscal
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.errors.use_cases.fiscal_not_authorized_error import FiscalNotAuthorizedError

class GetWorkProjectDocumentMobileController(ControllerInterface):
    def __init__(
        self,
        get_work_project_document_case: IGetWorkProjectDocument,
        get_work_project_case: IGetWorkProject,
        find_project_fiscal_case: IFindProjectFiscal
    ) -> None:
        self.__get_work_project_document_case = get_work_project_document_case
        self.__get_work_project_case = get_work_project_case
        self.__find_project_fiscal_case = find_project_fiscal_case

    def handle(self, http_request: HttpRequest) -> HttpResponse:
        try:
            path_params = http_request.path_params or {}
            body = http_request.body or {}

            work_project_id = int(path_params["work_project_id"])
            document_name = path_params["document_name"]
            fiscal_id = body.get("fiscal_id")

            # 1) Descobrir o project_id pelo work_project_id
            work_project = self.__get_work_project_case.get(work_project_id=work_project_id)
            project_id = work_project.project_id

            # 2) Validar que o fiscal está associado ao projeto
            try:
                self.__find_project_fiscal_case.find(project_id=project_id, fiscal_id=fiscal_id)
            except Exception as e:
                raise FiscalNotAuthorizedError(
                    title="FiscalNotAuthorizedError",
                    message=f"Fiscal {fiscal_id} não está autorizado a acessar documentos do projeto {project_id}."
                ) from e

            # 3) Obter o documento
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