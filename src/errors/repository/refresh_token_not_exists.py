from src.errors.use_cases.base.BaseError import BaseError

class RefreshTokenNotExists(BaseError):

    def __init__(self, message:str, *args, **kwargs) -> None:
        super().__init__(
            title='RefreshTokenNotExists',
            message=message,
            *args,
            **kwargs
        )