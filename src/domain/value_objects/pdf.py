from io import BytesIO

class PDF:

    def __init__(self, pdf: bytes):
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
    
    def __str__(self) -> str:
        return self.pdf.getvalue().hex()

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other) -> bool:
        if isinstance(other, PDF):
            return self.pdf.getvalue() == other.pdf.getvalue()
        return False