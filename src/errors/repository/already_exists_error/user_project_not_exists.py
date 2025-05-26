from src.errors.repository.__base.base_repository_error import BaseRepositoryError

class UserProjectNotExists(BaseRepositoryError):

    def __init__(self, message:str, *args, **kwargs) -> None:
        super().__init__(
            title='UserProjectNotExists',
            message=message,
            *args,
            **kwargs
        )