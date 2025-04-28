from src.errors.use_cases.base.BaseError import BaseError

class FiscalNotExists(BaseError):

    def __init__(self, message:str, *args, **kwargs) -> None:
        super().__init__(
            title='FiscalNotExists',
            message=message,
            *args,
            **kwargs
        )