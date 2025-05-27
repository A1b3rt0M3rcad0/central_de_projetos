from src.errors.repository.not_exists_error.__base_not_exists_error import BaseNotExistsError

class ProjectNotExistsError(BaseNotExistsError):

    def __init__(self, message:str, *args, **kwargs) -> None:
        super().__init__(
            title='ProjectIdNotExists',
            message=message,
            *args,
            **kwargs
        )