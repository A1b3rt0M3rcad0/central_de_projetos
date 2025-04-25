from src.data.interface.i_raven_project_document_repository import IProjectDocumentRepository
from src.domain.use_cases.i_delete_document import IDeleteDocument

class DeleteDocument(IDeleteDocument):

    def __init__(self, project_document_repository:IProjectDocumentRepository) -> None:
        self.__project_document_repository = project_document_repository
    
    def delete(self, project_id:int, document_name:str):
        try:
            self.__project_document_repository.delete_document(
                project_id=project_id,
                document_name=document_name
            )
        except Exception as e:
            raise e from e