from src.domain.use_cases.i_delete_fiscal_document import IDeleteFiscalDocument
from src.data.interface.i_project_document_fiscal_repository import IProjectDocumentFiscalRepository

class DeleteFiscalDocument(IDeleteFiscalDocument):

    def __init__(self, project_document_fiscal_repository:IProjectDocumentFiscalRepository):
        self.__project_document_fiscal_repository = project_document_fiscal_repository
    
    def delete(self, work_project_id:int, fiscal_id:int, document_name:str) -> None:
        try:
            self.__project_document_fiscal_repository.delete_fiscal_document(
                work_project_id=work_project_id,
                fiscal_id=fiscal_id,
                document_name=document_name
            )
        except Exception as e:
            raise RuntimeError(
                f'Erro ao deletar documento "{document_name}" do fiscal {fiscal_id} no work project {work_project_id}: {e}'
            ) from e 