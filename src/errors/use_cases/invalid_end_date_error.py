from src.errors.use_cases.base.BaseError import BaseError

class InvalidEndDateError(BaseError):

    def __init__(self, message:str, *args, **kwargs) -> None:
        super().__init__(
            title='InvalidEndDateError',
            message=message,
            *args,
            **kwargs
        )