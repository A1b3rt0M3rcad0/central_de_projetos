from src.errors.use_cases.base.BaseError import BaseError

class BairroNotExists(BaseError):

    def __init__(self, message:str, *args, **kwargs) -> None:
        super().__init__(
            title='BairroNotExists',
            message=message,
            *args,
            **kwargs
        )