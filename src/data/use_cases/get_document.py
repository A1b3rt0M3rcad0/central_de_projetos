from src.domain.value_objects.document import Document
from src.domain.use_cases.i_get_document import IGetDocument
from src.data.interface.i_raven_project_document_repository import IProjectDocumentRepository
from src.errors.use_cases.document_not_found_error import DocumentNotFoundError

class GetDocument(IGetDocument):

    def __init__(self, project_document_repository:IProjectDocumentRepository) -> None:
        self.__project_document_repository = project_document_repository
    
    def document(self, project_id:int, document_name:str, _document_class:Document = Document) -> Document:
        try:
            self.__project_document_repository.get_document(
                project_id=project_id,
                document_name=document_name,
                _document_class=_document_class
            )
        except AttributeError as e:
            raise DocumentNotFoundError(
                message=f'Document "{document_name}" not found in project "id:{project_id}": {e}'
            ) from e
        except Exception as e:
            raise e from e