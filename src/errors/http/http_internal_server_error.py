from src.errors.http.__http_base_error import HttpBaseError

class InternalServerError(HttpBaseError):

    def __init__(self, title:str, message:str) -> None:
        super().__init__(
            status_code=500,
            title=title,
            message=message
        )