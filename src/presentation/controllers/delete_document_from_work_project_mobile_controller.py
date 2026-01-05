from src.domain.use_cases.i_delete_fiscal_document_from_work_project import IDeleteFiscalDocumentFromWorkProject
from src.domain.use_cases.i_remove_document_from_work_project import IRemoveDocumentFromWorkProject
from src.domain.use_cases.i_get_work_project import IGetWorkProject
from src.domain.use_cases.i_verify_fiscal_work_project_association import IVerifyFiscalWorkProjectAssociation
from src.domain.use_cases.i_create_history_project import ICreateHistoryProject
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.errors.use_cases.unauthorized_access_error import UnauthorizedAccessError

class DeleteDocumentFromWorkProjectMobileController(ControllerInterface):
    
    def __init__(self, 
                 delete_fiscal_document_case: IDeleteFiscalDocumentFromWorkProject,
                 remove_document_from_work_project_case: IRemoveDocumentFromWorkProject,
                 get_work_project_case: IGetWorkProject,
                 verify_fiscal_work_project_association_case: IVerifyFiscalWorkProjectAssociation,
                 create_history_project_case: ICreateHistoryProject) -> None:
        self.__delete_fiscal_document_case = delete_fiscal_document_case
        self.__remove_document_from_work_project_case = remove_document_from_work_project_case
        self.__get_work_project_case = get_work_project_case
        self.__verify_fiscal_work_project_association_case = verify_fiscal_work_project_association_case
        self.__create_history_project_case = create_history_project_case
    
    def handle(self, http_request: HttpRequest) -> HttpResponse:
        try:
            body = http_request.body
            work_project_id = body['work_project_id']
            document_name = body['document_name']
            
            # Obter fiscal_id do body (vem do middleware de autenticação via form_data)
            fiscal_id = body.get('fiscal_id')
            
            if not fiscal_id:
                raise UnauthorizedAccessError(
                    message="Fiscal ID não encontrado na requisição"
                )
            
            # Validação: Verificar se o fiscal está associado ao work project
            is_associated = self.__verify_fiscal_work_project_association_case.verify(
                fiscal_id=fiscal_id,
                work_project_id=work_project_id
            )
            
            if not is_associated:
                raise UnauthorizedAccessError(
                    message=f"Fiscal não está autorizado a deletar documentos deste work project. Work Project ID: {work_project_id}"
                )
            
            # Validação: Verificar se o work_project existe e obter project_id
            work_project = None
            try:
                work_project = self.__get_work_project_case.get(work_project_id=work_project_id)
            except Exception as e:
                raise e from e
            
            # 1. Deletar o documento do RavenDB
            self.__delete_fiscal_document_case.delete(
                work_project_id=work_project_id,
                fiscal_id=fiscal_id,
                document_name=document_name
            )
            
            # 2. Remover o documento da lista de documentos do work project
            self.__remove_document_from_work_project_case.remove(
                work_project_id=work_project_id,
                document_name=document_name
            )
            
            # Criar histórico do projeto (usar project_id do work_project, não work_project_id)
            self.__create_history_project_case.create(
                project_id=work_project.project_id,
                data_name='Documento Mobile Deletado',
                description=f'Documento "{document_name}" deletado via mobile pelo fiscal {fiscal_id}'
            )
            
            return HttpResponse(
                status_code=200,
                body={
                    'message': f'Document "{document_name}" deleted successfully from work project {work_project_id}',
                    'work_project_id': work_project_id,
                    'fiscal_id': fiscal_id,
                    'document_name': document_name
                }
            )
            
        except Exception as e:
            raise e from e 