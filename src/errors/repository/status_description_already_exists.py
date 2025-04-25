from src.errors.use_cases.base.BaseError import BaseError

class StatusDescriptionAlreadyExists(BaseError):

    def __init__(self, message:str, *args, **kwargs) -> None:
        super().__init__(
            title='StatusDescriptionAlreadyExists',
            message=message,
            *args,
            **kwargs
        )