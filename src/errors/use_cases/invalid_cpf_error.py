from src.errors.use_cases.base.BaseError import BaseError

class InvalidCPFError(BaseError):

    def __init__(self, message:str, *args, **kwargs) -> None:
        super().__init__(
            title='InvalidCPFError',
            message=message,
            *args,
            **kwargs
        )