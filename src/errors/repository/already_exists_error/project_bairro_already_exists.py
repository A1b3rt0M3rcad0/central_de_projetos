from src.errors.repository.__base.base_repository_error import BaseRepositoryError

class ProjectBairroAlreadyExists(BaseRepositoryError):

    def __init__(self, message:str, *args, **kwargs) -> None:
        super().__init__(
            title='ProjectBairroAlreadyExists',
            message=message,
            *args,
            **kwargs
        )