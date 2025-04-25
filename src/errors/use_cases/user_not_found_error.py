from src.errors.use_cases.base.BaseError import BaseError

class UserNotFoundError(BaseError):

    def __init__(self, message:str, *args, **kwargs) -> None:
        super().__init__(
            title='UserNotFoundError',
            message=message,
            *args,
            **kwargs
        )