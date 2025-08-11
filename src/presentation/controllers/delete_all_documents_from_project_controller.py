from src.domain.use_cases.i_delete_all_documents_from_project import IDeleteAllDocumentsFromProject
from src.domain.use_cases.i_create_history_project import ICreateHistoryProject
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

class DeleteAllDocumentsFromProjectController(ControllerInterface):

    def __init__(self, 
                 delete_all_documents_from_project_case:IDeleteAllDocumentsFromProject,
                 create_history_project_case:ICreateHistoryProject) -> None:
        self.__delete_all_documents_from_project_case = delete_all_documents_from_project_case
        self.__create_history_project_case = create_history_project_case
    
    def handle(self, http_request:HttpRequest) -> HttpResponse:
        try:
            body = http_request.body
            project_id = body['project_id']
            
            # Deletar todos os documentos do projeto
            self.__delete_all_documents_from_project_case.delete(
                project_id=project_id
            )
            
            # Criar histórico do projeto
            self.__create_history_project_case.create(
                project_id=project_id,
                data_name='Documentos',
                description='Todos os documentos do projeto foram deletados'
            )
            
            return HttpResponse(
                status_code=200,
                body={
                    'message': 'All Documents from project deleted'
                }
            )
        except Exception as e:
            raise e from e