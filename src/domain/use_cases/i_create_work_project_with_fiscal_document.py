from abc import ABC, abstractmethod
from typing import List
from src.domain.value_objects.document import Document

class ICreateWorkProjectWithFiscalDocument(ABC):
    
    @abstractmethod
    def create_with_document(self, project_id:int, fiscal_id:int, title:str, description:str, documents:List[Document]) -> None:pass 