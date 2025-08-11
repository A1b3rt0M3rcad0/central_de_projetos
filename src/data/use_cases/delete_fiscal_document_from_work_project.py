from src.domain.use_cases.i_delete_fiscal_document_from_work_project import IDeleteFiscalDocumentFromWorkProject
from src.data.interface.i_project_document_fiscal_repository import IProjectDocumentFiscalRepository

class DeleteFiscalDocumentFromWorkProject(IDeleteFiscalDocumentFromWorkProject):

    def __init__(self, project_document_fiscal_repository: IProjectDocumentFiscalRepository) -> None:
        self.__project_document_fiscal_repository = project_document_fiscal_repository
    
    def delete(self, work_project_id: int, fiscal_id: int, document_name: str) -> None:
        try:
            self.__project_document_fiscal_repository.delete_fiscal_document(
                work_project_id=work_project_id,
                fiscal_id=fiscal_id,
                document_name=document_name
            )
        except Exception as e:
            raise e from e 