from src.domain.use_cases.i_get_work_project_document import IGetWorkProjectDocument
from src.data.interface.i_project_document_fiscal_repository import IProjectDocumentFiscalRepository

class GetWorkProjectDocument(IGetWorkProjectDocument):
    def __init__(self, project_document_fiscal_repository: IProjectDocumentFiscalRepository) -> None:
        self.__project_document_fiscal_repository = project_document_fiscal_repository

    def get_document(self, work_project_id: int, document_name: str) -> bytes:
        return self.__project_document_fiscal_repository.get_document_by_work_project_and_name(
            work_project_id=work_project_id,
            document_name=document_name
        ) 