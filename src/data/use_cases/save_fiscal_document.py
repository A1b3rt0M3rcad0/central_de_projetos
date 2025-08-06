#pylint:disable=W0611
from src.domain.use_cases.i_save_fiscal_document import ISaveFiscalDocument
from src.data.interface.i_project_document_fiscal_repository import IProjectDocumentFiscalRepository
from src.domain.value_objects.document import Document
from src.infra.raven.documents.project_document_fiscal import ProjectDocumentsFiscal
from typing import List

class SaveFiscalDocument(ISaveFiscalDocument):

    def __init__(self, project_document_fiscal_repository:IProjectDocumentFiscalRepository) -> None:
        self.__project_document_fiscal_repository = project_document_fiscal_repository
    
    def save(self, work_project_id:int, documents:List[Document]) -> None:
        try:
            self.__project_document_fiscal_repository.insert_fiscal_documents(
                work_project_id=work_project_id,
                documents=documents
            )
        except Exception as e:
            raise RuntimeError(
                f'Erro ao salvar documentos no work project {work_project_id}: {e}'
            ) from e 