from typing import List
from src.domain.use_cases.i_get_fiscal_document_names import IGetFiscalDocumentNames
from src.data.interface.i_project_document_fiscal_repository import IProjectDocumentFiscalRepository

class GetFiscalDocumentNames(IGetFiscalDocumentNames):

    def __init__(self, project_document_fiscal_repository:IProjectDocumentFiscalRepository) -> None:
        self.__project_document_fiscal_repository = project_document_fiscal_repository
    
    def get_names(self, project_id:int, fiscal_id:int) -> List[str]:
        try:
            result = self.__project_document_fiscal_repository.get_fiscal_document_names(
                project_id=project_id,
                fiscal_id=fiscal_id
            )
            return result
        except Exception as e:
            raise e from e 