from src.errors.repository.__base.base_repository_error import BaseRepositoryError

class ProjectsFromBairroDoesNotExists(BaseRepositoryError):

    def __init__(self, message:str, *args, **kwargs) -> None:
        super().__init__(
            title='ProjectsFromBairroDoesNotExists',
            message=message,
            *args,
            **kwargs
        )