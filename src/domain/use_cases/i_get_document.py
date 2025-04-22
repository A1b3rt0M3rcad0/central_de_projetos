from src.domain.value_objects.document import Document
from abc import ABC, abstractmethod

class IGetDocument(ABC):

    @abstractmethod
    def document(self, project_id:int, document_name:str, _document_class:Document=Document) -> Document:
        '''
        Coleta o project_id o document_name para retornar o documento buscado,
        Caso não encontre o documento, retorne 401, DocumentNotFoundedError
        '''