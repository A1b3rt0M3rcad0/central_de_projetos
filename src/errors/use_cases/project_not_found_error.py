from src.errors.use_cases.base.BaseError import BaseError

class ProjectNotFoundError(BaseError):

    def __init__(self, message:str, *args, **kwargs) -> None:
        super().__init__(
            title='ProjectNotFoundError',
            message=message,
            *args,
            **kwargs
        )