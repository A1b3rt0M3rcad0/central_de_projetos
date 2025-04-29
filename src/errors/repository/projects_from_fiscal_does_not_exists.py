from src.errors.use_cases.base.BaseError import BaseError

class ProjectsFromFiscalDoesNotExists(BaseError):

    def __init__(self, message:str, *args, **kwargs) -> None:
        super().__init__(
            title='ProjectsFromFiscalDoesNotExists',
            message=message,
            *args,
            **kwargs
        )