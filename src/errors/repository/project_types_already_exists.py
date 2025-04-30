from src.errors.use_cases.base.BaseError import BaseError

class ProjectTypesAlreadyExists(BaseError):

    def __init__(self, message:str, *args, **kwargs) -> None:
        super().__init__(
            title=self.__class__.__name__,
            message=message,
            *args,
            **kwargs
        )