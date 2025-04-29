from src.errors.use_cases.base.BaseError import BaseError

class ErrorOnUpdateBairroFromProject(BaseError):

    def __init__(self, message:str, *args, **kwargs) -> None:
        super().__init__(
            title='ErrorOnUpdateBairroFromProject',
            message=message,
            *args,
            **kwargs
        )