from src.errors.repository.not_exists_error.__base_not_exists_error import BaseNotExistsError

class WorkProjectNotExists(BaseNotExistsError):

    def __init__(self, message:str, *args, **kwargs) -> None:
        super().__init__(
            title='WorkProjectNotExists',
            message=message,
            *args,
            **kwargs
        ) 