from src.errors.repository.already_exists_error.__base_already_exists_error import BaseAlreadyExistsError

class UserAlreadyExists(BaseAlreadyExistsError):

    def __init__(self, message:str, *args, **kwargs) -> None:
        super().__init__(
            title='UserAlreadyExists',
            message=message,
            *args,
            **kwargs
        )