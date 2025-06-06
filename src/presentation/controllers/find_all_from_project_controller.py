from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.domain.use_cases.i_find_all_from_project import IFindAllFromProject
from src.domain.use_cases.I_get_document_names import IGetDocumentNames
from src.presentation.interface.controller_interface import ControllerInterface
from src.domain.entities.project import ProjectEntity

class FindAllFromProjectController(ControllerInterface):

    def __init__(self, find_all_from_project_case:IFindAllFromProject, get_document_names_case:IGetDocumentNames) -> None:
        self.__find_all_from_project_case = find_all_from_project_case
        self.__get_document_names_case = get_document_names_case
    
    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            path_params = http_request.path_params
            project_id = path_params["project_id"]
            result:ProjectEntity = self.__find_all_from_project_case.find(project_id=project_id)
            documents = self.__get_document_names_case.names(project_id=project_id)
            return HttpResponse(
                status_code=200,
                body={
                    "message": "Project Founded",
                    "content": {
                        "id": result.project_id,
                        "name": result.name,
                        "status": {
                            "id": result.status.status_id,
                            "description": result.status.description,
                            "created_at": result.status.created_at.strftime(r'%d/%m/%Y')
                        } if result.status is not None else None,
                        "bairro": {
                            "id": result.bairro.bairro,
                            "name": result.bairro.name,
                            "created_at": result.bairro.created_at.strftime(r'%d/%m/%Y')
                        } if result.bairro is not None else None,
                        "empresa": {
                            "id": result.empresas.empresa_id,
                            "name": result.empresas.name,
                            "created_at": result.empresas.created_at.strftime(r'%d/%m/%Y')
                        } if result.empresas is not None else None,
                        "fiscal": {
                            "id": result.fiscal.fiscal_id,
                            "name": result.fiscal.name,
                            "created_at": result.fiscal.created_at.strftime(r'%d/%m/%Y')
                        } if result.fiscal is not None else None,
                        "types": {
                            "id": result.types.types_id,
                            "name": result.types.name,
                            "created_at": result.types.created_at.strftime(r'%d/%m/%Y')
                        } if result.types is not None else None,
                        "history_project": [
                            {
                                "id": history.history_project_id,
                                "project_id": history.project_id,
                                "description": history.description,
                                "data_name": history.data_name,
                                "updated_at": history.updated_at.strftime(r'%d/%m/%Y')
                            } for history in result.history_project
                        ] if result.history_project is not None else [],
                        "andamento_do_projeto": result.andamento_do_projeto,
                        "expected_completion_date": result.expected_completion_date.strftime(r'%d/%m/%Y') if result.expected_completion_date else result.expected_completion_date,
                        "end_date": result.end_date.strftime(r'%d/%m/%Y') if result.end_date else result.end_date,
                        "start_date": result.start_date.strftime(r'%d/%m/%Y') if result.start_date else result.start_date,
                        "verba_disponivel": result.verba_disponivel,
                        "documents": documents
                    }
                }
            )
        except Exception as e:
            raise e from e
