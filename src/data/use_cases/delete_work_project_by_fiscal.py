from src.domain.use_cases.i_delete_work_project_by_fiscal import IDeleteWorkProjectByFiscal
from src.data.interface.i_work_project_repository import IWorkProjectRepository
from src.data.interface.i_project_document_fiscal_repository import IProjectDocumentFiscalRepository
from src.errors.use_cases.fiscal_not_authorized_error import FiscalNotAuthorizedError
from src.errors.repository.not_exists_error.work_project_not_exists import WorkProjectNotExists

class DeleteWorkProjectByFiscal(IDeleteWorkProjectByFiscal):

    def __init__(self, 
                 work_project_repository:IWorkProjectRepository,
                 project_document_fiscal_repository:IProjectDocumentFiscalRepository) -> None:
        self.__work_project_repository = work_project_repository
        self.__project_document_fiscal_repository = project_document_fiscal_repository
    
    def delete(self, work_project_id:int, fiscal_id:int) -> None:
        try:
            # Primeiro, buscar o work project para verificar se existe e se o fiscal está autorizado
            work_project = self.__work_project_repository.find(work_project_id=work_project_id)
            
            # Verificar se o fiscal está associado ao work project
            if work_project.fiscal_id != fiscal_id:
                raise FiscalNotAuthorizedError(
                    title="FiscalNotAuthorizedError",
                    message=f'Fiscal {fiscal_id} não está autorizado a deletar o work project {work_project_id}. Apenas o fiscal associado pode deletar o work project.'
                )
            
            # Deletar todos os documentos fiscais associados ao work project
            self.__project_document_fiscal_repository.delete_all_fiscal_documents_from_work_project(
                work_project_id=work_project_id,
                fiscal_id=fiscal_id
            )
            
            # Deletar o work project
            self.__work_project_repository.delete(work_project_id=work_project_id)
            
        except WorkProjectNotExists:
            raise
        except FiscalNotAuthorizedError:
            raise
        except Exception as e:
            raise e from e 