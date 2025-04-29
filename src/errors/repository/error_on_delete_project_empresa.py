from src.errors.use_cases.base.BaseError import BaseError

class ErrorOnDeleteProjectEmpresa(BaseError):

    def __init__(self, message:str, *args, **kwargs) -> None:
        super().__init__(
            title='ErrorOnDeleteProjectEmpresa',
            message=message,
            *args,
            **kwargs
        )