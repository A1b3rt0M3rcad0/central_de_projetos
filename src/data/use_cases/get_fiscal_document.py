#pylint:disable=E0611
from src.domain.value_objects.document import Document
from src.domain.use_cases.i_get_fiscal_document import IGetFiscalDocument
from src.data.interface.i_project_document_fiscal_repository import IProjectDocumentFiscalRepository

from src.errors.use_cases.fiscal_document_not_found_error import FiscalDocumentNotFoundError

class GetFiscalDocument(IGetFiscalDocument):

    def __init__(self, project_document_fiscal_repository:IProjectDocumentFiscalRepository) -> None:
        self.__project_document_fiscal_repository = project_document_fiscal_repository
    
    def get(self, work_project_id:int, fiscal_id:int, document_name:str) -> Document:
        try:
            document = self.__project_document_fiscal_repository.get_fiscal_document(
                work_project_id=work_project_id,
                fiscal_id=fiscal_id,
                document_name=document_name
            )
            if document is None:
                raise FiscalDocumentNotFoundError(
                    message=f'Documento "{document_name}" do fiscal {fiscal_id} não encontrado no work project {work_project_id}'
                )
            return document
        except AttributeError as e:
            raise FiscalDocumentNotFoundError(
                message=f'Documento "{document_name}" do fiscal {fiscal_id} não encontrado no work project {work_project_id}: {e}'
            ) from e
        except Exception as e:
            raise e from e 