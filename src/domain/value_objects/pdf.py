from io import BytesIO
from src.domain.value_objects.document import Document

class PDF(Document):

    def __init__(self, pdf: bytes, document_name:str|None=None):
        self.document_name = document_name
        self.__pdf = BytesIO(pdf)
        self.__content_type = "application/pdf"
        self.__name = "document.pdf"

    @property
    def pdf(self) -> BytesIO:
        return self.__pdf
    
    @property
    def content_type(self) -> str:
        return self.__content_type
    
    @property
    def name(self) -> str:
        return self.__name
    
    def value(self) -> bytes:
        return self.__pdf.getvalue()
    
    def to_dict(self) -> dict:
        return {
            'document': self.value(),
            'content_type': self.__content_type,
            'document_name': self.document_name,
            'name': self.__name
        }
    
    def __str__(self) -> str:
        return self.pdf.getvalue().hex()

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other) -> bool:
        if isinstance(other, PDF):
            return self.pdf.getvalue() == other.pdf.getvalue()
        return False