from typing import List
from src.domain.use_cases.I_get_document_names import IGetDocumentNames
from src.data.interface.i_raven_project_document_repository import IProjectDocumentRepository

class GetDocumentNames(IGetDocumentNames):

    def __init__(self, project_documents_repository:IProjectDocumentRepository) -> None:
        self.__project_documents_repository = project_documents_repository
    
    def names(self, project_id:int) -> List[str]:
        try:
            result = self.__project_documents_repository.get_document_names(
                project_id=project_id
            )
            return result
        except Exception as e:
            raise e from e