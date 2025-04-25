from src.errors.use_cases.base.BaseError import BaseError

class InvalidEmailError(BaseError):

    def __init__(self, message:str, *args, **kwargs) -> None:
        super().__init__(
            title='InvalidEmailError',
            message=message,
            *args,
            **kwargs
        )