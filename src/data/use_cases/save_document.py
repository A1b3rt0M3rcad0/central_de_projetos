from src.domain.use_cases.i_save_document import ISaveDocument
from src.data.interface.i_raven_project_document_repository import IProjectDocumentRepository
from src.domain.value_objects.document import Document
from src.infra.raven.documents.project_documents import ProjectDocuments
from typing import List

class SaveDocument(ISaveDocument):

    def __init__(self, project_document_repository:IProjectDocumentRepository) -> None:
        self.__project_document_repository = project_document_repository
    
    def save(self, project_id:int, document:List[Document]) -> None:
        try:
            self.__project_document_repository.insert_documents(
                project_id=project_id,
                project_documents=ProjectDocuments(),
                documents=document
            )
        except Exception as e:
            raise RuntimeError(
                f'Erro ao inserir um novo dado ao projeto {project_id}: {e}'
            ) from e