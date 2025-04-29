from src.errors.use_cases.base.BaseError import BaseError

class FiscalAlreadyExists(BaseError):

    def __init__(self, message:str, *args, **kwargs) -> None:
        super().__init__(
            title='FiscalAlreadyExists',
            message=message,
            *args,
            **kwargs
        )