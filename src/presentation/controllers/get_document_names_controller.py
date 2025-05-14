from src.domain.use_cases.I_get_document_names import IGetDocumentNames
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

class GetDocumentNamesController(ControllerInterface):

    def __init__(self, get_document_names_case:IGetDocumentNames) -> None:
        self.__get_document_names_case = get_document_names_case
    
    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            query_params = http_request.query_params
            project_id = query_params['project_id']
            names = self.__get_document_names_case.names(
                project_id=project_id
            )
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'projects_founded',
                    'content': names
                }
            )
        except Exception as e:
            raise e from e