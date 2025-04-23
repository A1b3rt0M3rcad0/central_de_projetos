from src.errors.use_cases.base.BaseError import BaseError

class CreateUserError(BaseError):

    def __init__(self, message:str, *args, **kwargs) -> None:
        super().__init__(
            title='CreateUserError',
            message=message,
            *args,
            **kwargs
        )