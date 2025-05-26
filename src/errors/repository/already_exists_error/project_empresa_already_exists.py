from src.errors.repository.__base.base_repository_error import BaseRepositoryError

class ProjectEmpresaAlreadyExists(BaseRepositoryError):

    def __init__(self, message:str, *args, **kwargs) -> None:
        super().__init__(
            title='ProjectEmpresaAlreadyExists',
            message=message,
            *args,
            **kwargs
        )