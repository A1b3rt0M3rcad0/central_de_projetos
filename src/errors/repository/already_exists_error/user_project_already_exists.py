from src.errors.repository.already_exists_error.__base_already_exists_error import BaseAlreadyExistsError

class UserProjectAlreadyExists(BaseAlreadyExistsError):

    def __init__(self, message:str, *args, **kwargs) -> None:
        super().__init__(
            title=self.__class__.__name__,
            message=message,
            *args,
            **kwargs
        )