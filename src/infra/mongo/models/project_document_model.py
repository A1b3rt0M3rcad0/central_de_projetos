from src.domain.value_objects.excel import Excel
from src.domain.value_objects.pdf import PDF
from src.domain.value_objects.word import Word
from typing import Union, List

class ProjectDocumentModel:

    def __init__(self, project_id:int, documents: List[Union[Excel, PDF, Word]]) -> None:
        self.__project_id = project_id
        self.__documents = documents
    
    @property
    def documents(self) -> List[Union[Excel, PDF, Word]]:
        return self.__documents
    
    @property
    def project_id(self) -> int:
        return self.__project_id
    
    def __eq__(self, other):
        if not isinstance(other, ProjectDocumentModel):
            return False
        return self.project_id == other.project_id and self.documents == other.documents
