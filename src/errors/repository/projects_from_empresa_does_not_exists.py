from src.errors.use_cases.base.BaseError import BaseError

class ProjectsFromEmpresaDoesNotExists(BaseError):

    def __init__(self, message:str, *args, **kwargs) -> None:
        super().__init__(
            title='ProjectsFromEmpresaDoesNotExists',
            message=message,
            *args,
            **kwargs
        )