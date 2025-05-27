from src.errors.repository.already_exists_error.__base_already_exists_error import BaseAlreadyExistsError

class ProjectBairroAlreadyExists(BaseAlreadyExistsError):

    def __init__(self, message:str, *args, **kwargs) -> None:
        super().__init__(
            title='ProjectBairroAlreadyExists',
            message=message,
            *args,
            **kwargs
        )