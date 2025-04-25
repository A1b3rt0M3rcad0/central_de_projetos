from src.errors.use_cases.base.BaseError import BaseError

class StatusNotFoundError(BaseError):

    def __init__(self, message:str, *args, **kwargs) -> None:
        super().__init__(
            title='StatusNotFoundError',
            message=message,
            *args,
            **kwargs
        )