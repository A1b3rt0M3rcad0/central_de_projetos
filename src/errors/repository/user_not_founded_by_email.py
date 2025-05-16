from src.errors.use_cases.base.BaseError import BaseError

class UserNotFoundedByEmail(BaseError):

    def __init__(self, message:str, *args, **kwargs) -> None:
        super().__init__(
            title='UserNotFoundedByEmail',
            message=message,
            *args,
            **kwargs
        )