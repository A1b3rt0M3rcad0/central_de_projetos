from src.errors.use_cases.base.BaseError import BaseError

class ProjectIdNotExistsError(BaseError):

    def __init__(self, message:str, *args, **kwargs) -> None:
        super().__init__(
            title='ProjectIdNotExists',
            message=message,
            *args,
            **kwargs
        )