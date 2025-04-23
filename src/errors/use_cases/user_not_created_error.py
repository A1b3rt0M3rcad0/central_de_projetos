from src.errors.use_cases.base.BaseError import BaseError

class UserNotCreatedError(BaseError):

    def __init__(self, message:str, *args, **kwargs) -> None:
        super().__init__(
            title='UserNotCreatedError',
            message=message,
            *args,
            **kwargs
        )