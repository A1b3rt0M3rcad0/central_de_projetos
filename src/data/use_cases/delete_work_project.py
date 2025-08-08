from src.domain.use_cases.i_delete_work_project import IDeleteWorkProject
from src.data.interface.i_work_project_repository import IWorkProjectRepository
from src.data.interface.i_project_document_fiscal_repository import IProjectDocumentFiscalRepository
from src.errors.use_cases.delete_work_project_error import DeleteWorkProjectError

class DeleteWorkProject(IDeleteWorkProject):
    
    def __init__(self, 
                 work_project_repository:IWorkProjectRepository,
                 project_document_fiscal_repository:IProjectDocumentFiscalRepository) -> None:
        self.__work_project_repository = work_project_repository
        self.__project_document_fiscal_repository = project_document_fiscal_repository
    
    def delete(self, work_project_id:int) -> None:
        try:
            # Primeiro, buscar o work project para obter o fiscal_id
            work_project = self.__work_project_repository.find(work_project_id)
            
            # Deletar todos os documentos fiscais relacionados ao work project
            self.__project_document_fiscal_repository.delete_all_fiscal_documents_from_work_project(
                work_project_id=work_project_id,
                fiscal_id=work_project.fiscal_id
            )
            
            # Deletar o work project da tabela relacional
            self.__work_project_repository.delete(work_project_id=work_project_id)
            
        except Exception as e:
            raise DeleteWorkProjectError(
                message=f'Erro ao deletar work project {work_project_id}: {e}'
            ) from e 