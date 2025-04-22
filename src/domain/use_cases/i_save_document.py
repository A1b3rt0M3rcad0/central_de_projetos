from src.domain.value_objects.document import Document
from typing import List
from abc import ABC, abstractmethod

class ISaveDocument(ABC):

    @abstractmethod
    def save(self, project_id:int, document:List[Document]) -> None:
        '''
        Pega o project_id e a lista de documents, para realizar a adição dos documentos no banco de dados do projeto,
        caso não consiga salvar o document, retorne 500, FileSaveError
        '''