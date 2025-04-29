from src.errors.use_cases.base.BaseError import BaseError

class ProjectsFromBairroDoesNotExists(BaseError):

    def __init__(self, message:str, *args, **kwargs) -> None:
        super().__init__(
            title='ProjectsFromBairroDoesNotExists',
            message=message,
            *args,
            **kwargs
        )