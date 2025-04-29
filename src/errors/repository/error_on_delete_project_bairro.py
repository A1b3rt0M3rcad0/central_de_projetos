from src.errors.use_cases.base.BaseError import BaseError

class ErrorOnDeleteProjectBairro(BaseError):

    def __init__(self, message:str, *args, **kwargs) -> None:
        super().__init__(
            title='ErrorOnDeleteProjectBairro',
            message=message,
            *args,
            **kwargs
        )