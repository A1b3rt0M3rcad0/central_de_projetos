from src.errors.use_cases.base.BaseError import BaseError

class CPFOrEmailAlreadyExists(BaseError):

    def __init__(self, message:str, *args, **kwargs) -> None:
        super().__init__(
            title='CPFOrEmailAlreadyExists',
            message=message,
            *args,
            **kwargs
        )