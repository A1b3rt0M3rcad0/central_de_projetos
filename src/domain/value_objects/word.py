from io import BytesIO

class Word:

    def __init__(self, docx: bytes, document_name:str|None=None):
        self.document_name = document_name
        self.__docx = BytesIO(docx)
        self.__content_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        self.__name = "document.docx"

    @property
    def docx(self) -> BytesIO:
        return self.__docx

    @property
    def content_type(self) -> str:
        return self.__content_type

    @property
    def name(self) -> str:
        return self.__name
    
    def value(self) -> bytes:
        return self.__docx.getvalue()

    def __str__(self) -> str:
        return self.docx.getvalue().hex()

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other) -> bool:
        if isinstance(other, Word):
            return self.docx.getvalue() == other.docx.getvalue()
        return False