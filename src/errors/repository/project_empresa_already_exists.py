from src.errors.use_cases.base.BaseError import BaseError

class ProjectEmpresaAlreadyExists(BaseError):

    def __init__(self, message:str, *args, **kwargs) -> None:
        super().__init__(
            title='ProjectEmpresaAlreadyExists',
            message=message,
            *args,
            **kwargs
        )