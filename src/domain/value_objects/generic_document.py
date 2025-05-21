from src.domain.value_objects.document import Document


class GenericDocument(Document):
    def __init__(self, document: bytes, content_type: str, name: str, document_name: str):
        self.__document = document
        self.__content_type = content_type
        self.__name = name
        self.__document_name = document_name

    @property
    def content_type(self) -> str:
        return self.__content_type

    @property
    def name(self) -> str:
        return self.__name

    @property
    def document_name(self) -> str:
        return self.__document_name

    def value(self) -> bytes:
        return self.__document

    def to_dict(self) -> dict:
        return {
            'document': self.value(),
            'content_type': self.content_type,
            'document_name': self.document_name,
            'name': self.name
        }