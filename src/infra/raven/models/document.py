from src.domain.value_objects.document import Document

class DocumentModel:

    def __init__(self, _document_class:Document) -> None:
        self._document_class = _document_class
    
    def make_document(self, document_name:str, document_value:bytes) -> Document:
        document = self._document_class(document_value, document_name=document_name)
        return document