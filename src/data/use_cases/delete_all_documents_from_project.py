from src.domain.use_cases.i_delete_all_documents_from_project import IDeleteAllDocumentsFromProject
from src.data.interface.i_raven_project_document_repository import IProjectDocumentRepository

class DeleteAllDocumentsFromProject(IDeleteAllDocumentsFromProject):

    def __init__(self, project_document_repository:IProjectDocumentRepository):
        self.__project_document_repository =project_document_repository
    
    def delete(self, project_id:int) -> None:
        try:
            self.__project_document_repository.delete_project(
                project_id=project_id
            )
        except Exception as e:
            raise e from e