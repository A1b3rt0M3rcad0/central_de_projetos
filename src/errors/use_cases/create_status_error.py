from src.errors.use_cases.base.BaseError import BaseError

class CreateStatusError(BaseError):

    def __init__(self, message:str, *args, **kwargs) -> None:
        super().__init__(
            title='CreateStatusError',
            message=message,
            *args,
            **kwargs
        )