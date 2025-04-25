from src.errors.use_cases.base.BaseError import BaseError

class StatusDescriptionError(BaseError):

    def __init__(self, message:str, *args, **kwargs) -> None:
        super().__init__(
            title='StatusDescriptionError',
            message=message,
            *args,
            **kwargs
        )