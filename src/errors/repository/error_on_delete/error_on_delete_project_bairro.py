from src.errors.repository.__base.base_repository_error import BaseRepositoryError

class ErrorOnDeleteProjectBairro(BaseRepositoryError):

    def __init__(self, message:str, *args, **kwargs) -> None:
        super().__init__(
            title='ErrorOnDeleteProjectBairro',
            message=message,
            *args,
            **kwargs
        )