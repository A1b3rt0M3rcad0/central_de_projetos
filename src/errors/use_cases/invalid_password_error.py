from src.errors.use_cases.base.BaseError import BaseError

class InvalidPasswordError(BaseError):

    def __init__(self, message:str, *args, **kwargs) -> None:
        super().__init__(
            title='InvalidPasswordError',
            message=message,
            *args,
            **kwargs
        )