from src.errors.use_cases.base.BaseError import BaseError

class ErrorOnUpdateFiscalFromProject(BaseError):

    def __init__(self, message:str, *args, **kwargs) -> None:
        super().__init__(
            title='ErrorOnUpdateFiscalFromProject',
            message=message,
            *args,
            **kwargs
        )