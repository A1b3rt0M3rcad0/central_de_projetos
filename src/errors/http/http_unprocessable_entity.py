from src.errors.http.__http_base_error import HttpBaseError

class UnprocessalbeEntity(HttpBaseError):

    def __init__(self, title:str, message:str) -> None:
        super().__init__(
            status_code=422,
            title=title,
            message=message
        )