from src.errors.repository.__base.base_repository_error import BaseRepositoryError

class BairroAlreadyExists(BaseRepositoryError):

    def __init__(self, message:str, *args, **kwargs) -> None:
        super().__init__(
            title='BairroAlreadyExists',
            message=message,
            *args,
            **kwargs
        )