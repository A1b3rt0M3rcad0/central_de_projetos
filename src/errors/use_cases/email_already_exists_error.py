from src.errors.use_cases.base.BaseError import BaseError

class EmailAlreadyExistsError(BaseError):

    def __init__(self, message:str, *args, **kwargs) -> None:
        super().__init__(
            title='EmailAlreadyExistsError',
            message=message,
            *args,
            **kwargs
        )