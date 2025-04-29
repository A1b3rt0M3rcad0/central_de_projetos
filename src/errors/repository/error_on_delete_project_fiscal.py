from src.errors.use_cases.base.BaseError import BaseError

class ErrorOnDeleteProjectFiscal(BaseError):

    def __init__(self, message:str, *args, **kwargs) -> None:
        super().__init__(
            title='ErrorOnDeleteProjectFiscal',
            message=message,
            *args,
            **kwargs
        )