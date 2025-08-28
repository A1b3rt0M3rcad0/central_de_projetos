from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.domain.use_cases.i_find_all_from_project import IFindAllFromProject
from src.domain.use_cases.i_find_user_by_project_id import IFindUserByProjectId
from src.domain.use_cases.I_get_document_names import IGetDocumentNames
from src.presentation.interface.controller_interface import ControllerInterface
from src.domain.entities.project import ProjectEntity

class FindAllFromProjectController(ControllerInterface):

    def __init__(self, find_all_from_project_case:IFindAllFromProject, get_document_names_case:IGetDocumentNames, find_user_by_project_id:IFindUserByProjectId) -> None:
        self.__find_all_from_project_case = find_all_from_project_case
        self.__get_document_names_case = get_document_names_case
        self.__find_user_by_project_id_case = find_user_by_project_id
    
    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            path_params = http_request.path_params
            project_id = path_params["project_id"]
            result:ProjectEntity = self.__find_all_from_project_case.find(project_id=project_id)
            documents = self.__get_document_names_case.names(project_id=project_id)
            user = self.__find_user_by_project_id_case.find(project_id=project_id)
            return HttpResponse(
                status_code=200,
                body={
                    "message": "Project Founded",
                    "content": {
                        "id": result.project_id,
                        "name": result.name,
                        "status": self._format_status(result.status),
                        "bairro": self._format_association(result.bairro, "bairro"),
                        "empresa": self._format_association(result.empresas, "empresa_id"),
                        "fiscal": self._format_association(result.fiscal, "fiscal_id"),
                        "types": self._format_association(result.types, "types_id"),
                        "history_project": self._format_history_project(result.history_project),
                        "andamento_do_projeto": result.andamento_do_projeto,
                        "expected_completion_date": result.expected_completion_date.strftime(r'%d/%m/%Y') if result.expected_completion_date else result.expected_completion_date,
                        "end_date": result.end_date.strftime(r'%d/%m/%Y') if result.end_date else result.end_date,
                        "start_date": result.start_date.strftime(r'%d/%m/%Y') if result.start_date else result.start_date,
                        "verba_disponivel": float(result.verba_disponivel) if result.verba_disponivel is not None else None,
                        "documents": documents,
                        "user": {"cpf": user.cpf.value, "name": user.name} if user else None
                    }
                }
            )
        except Exception as e:
            raise e from e
    
    def _format_association(self, association, id_field):
        """Formata uma associação sempre como lista, mesmo que seja apenas um objeto individual"""
        if isinstance(association, list):
            # Se já é uma lista, retorna lista de objetos formatados
            return [
                {
                    "id": getattr(item, id_field),
                    "name": item.name,
                    "created_at": item.created_at.strftime(r'%d/%m/%Y')
                } for item in association
            ]
        if association is not None:
            # Se é um objeto individual, retorna lista com um elemento
            return [
                {
                    "id": getattr(association, id_field),
                    "name": association.name,
                    "created_at": association.created_at.strftime(r'%d/%m/%Y')
                }
            ]
        # Se é None, retorna lista vazia
        return []
    
    def _format_history_project(self, history_project):
        """Formata o histórico do projeto sempre como lista"""
        if history_project is not None:
            return [
                {
                    "id": history.history_project_id,
                    "project_id": history.project_id,
                    "description": history.description,
                    "data_name": history.data_name,
                    "updated_at": history.updated_at.strftime(r'%d/%m/%Y')
                } for history in history_project
            ]
        return []
    
    def _format_status(self, status):
        """Formata o status do projeto"""
        if status is not None:
            return {
                "id": status.status_id,
                "description": status.description,
                "created_at": status.created_at.strftime(r'%d/%m/%Y')
            }
        return None
