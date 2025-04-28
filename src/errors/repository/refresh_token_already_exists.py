from src.errors.use_cases.base.BaseError import BaseError

class RefreshTokenAlreadyExists(BaseError):

    def __init__(self, message:str, *args, **kwargs) -> None:
        super().__init__(
            title='RefreshTokenAlreadyExists',
            message=message,
            *args,
            **kwargs
        )