from io import BytesIO
from src.domain.value_objects.document import Document

class Excel(Document):

    def __init__(self, xlsx: bytes, document_name:str|None=None):
        self.document_name = document_name
        self.__xlsx = BytesIO(xlsx)
        self.__content_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        self.__name = "document.xlsx"

    @property
    def xlsx(self) -> BytesIO:
        return self.__xlsx

    @property
    def content_type(self) -> str:
        return self.__content_type

    @property
    def name(self) -> str:
        return self.__name
    
    def value(self) -> bytes:
        return self.__xlsx.getvalue()
    
    def to_dict(self) -> dict:
        return {
            'document': self.value(),
            'content_type': self.__content_type,
            'document_name': self.document_name,
            'name': self.__name
        }

    def __str__(self) -> str:
        return self.xlsx.getvalue().hex()

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other) -> bool:
        if isinstance(other, Excel):
            return self.xlsx.getvalue() == other.xlsx.getvalue()
        return False
