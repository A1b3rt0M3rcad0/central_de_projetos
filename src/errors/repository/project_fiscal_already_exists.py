from src.errors.use_cases.base.BaseError import BaseError

class ProjectFiscalAlreadyExists(BaseError):

    def __init__(self, message:str, *args, **kwargs) -> None:
        super().__init__(
            title='ProjectFiscalAlreadyExists',
            message=message,
            *args,
            **kwargs
        )