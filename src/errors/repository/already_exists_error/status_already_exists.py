from src.errors.repository.already_exists_error.__base_already_exists_error import BaseAlreadyExistsError

class StatusAlreadyExists(BaseAlreadyExistsError):

    def __init__(self, message:str, *args, **kwargs) -> None:
        super().__init__(
            title='StatusDescriptionAlreadyExists',
            message=message,
            *args,
            **kwargs
        )