from src.errors.use_cases.base.BaseError import BaseError

class FileSaveError(BaseError):

    def __init__(self, message:str, *args, **kwargs) -> None:
        super().__init__(
            title='FileSaveError',
            message=message,
            *args,
            **kwargs
        )