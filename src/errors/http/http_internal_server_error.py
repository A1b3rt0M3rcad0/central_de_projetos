from src.errors.http.base.BaseError import BaseError

class InternalServerError(BaseError):

    def __init__(self, title:str, message:str) -> None:
        super().__init__(
            status_code=500,
            title=title,
            message=message
        )