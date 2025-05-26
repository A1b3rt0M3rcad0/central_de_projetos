from src.errors.repository.__base.base_repository_error import BaseRepositoryError

class ProjectFiscalAlreadyExists(BaseRepositoryError):

    def __init__(self, message:str, *args, **kwargs) -> None:
        super().__init__(
            title='ProjectFiscalAlreadyExists',
            message=message,
            *args,
            **kwargs
        )