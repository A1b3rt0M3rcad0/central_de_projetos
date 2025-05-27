from src.errors.repository.already_exists_error.__base_already_exists_error import BaseAlreadyExistsError

class UserProjectNotExists(BaseAlreadyExistsError):

    def __init__(self, message:str, *args, **kwargs) -> None:
        super().__init__(
            title='UserProjectNotExists',
            message=message,
            *args,
            **kwargs
        )