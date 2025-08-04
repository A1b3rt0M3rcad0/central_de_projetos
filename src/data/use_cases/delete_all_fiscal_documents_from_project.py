from src.domain.use_cases.i_delete_all_fiscal_documents_from_project import IDeleteAllFiscalDocumentsFromProject
from src.data.interface.i_project_document_fiscal_repository import IProjectDocumentFiscalRepository

class DeleteAllFiscalDocumentsFromProject(IDeleteAllFiscalDocumentsFromProject):

    def __init__(self, project_document_fiscal_repository:IProjectDocumentFiscalRepository):
        self.__project_document_fiscal_repository = project_document_fiscal_repository
    
    def delete_all(self, work_project_id:int, fiscal_id:int) -> None:
        try:
            self.__project_document_fiscal_repository.delete_all_fiscal_documents_from_work_project(
                work_project_id=work_project_id,
                fiscal_id=fiscal_id
            )
        except Exception as e:
            raise RuntimeError(
                f'Erro ao deletar todos os documentos do fiscal {fiscal_id} no work project {work_project_id}: {e}'
            ) from e 