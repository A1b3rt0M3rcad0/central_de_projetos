from src.errors.use_cases.base.BaseError import BaseError

class ProjectBairroAlreadyExists(BaseError):

    def __init__(self, message:str, *args, **kwargs) -> None:
        super().__init__(
            title='ProjectBairroAlreadyExists',
            message=message,
            *args,
            **kwargs
        )