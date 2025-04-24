from src.errors.use_cases.base.BaseError import BaseError

class RegistryAlreadyExists(BaseError):

    def __init__(self, message:str, *args, **kwargs) -> None:
        super().__init__(
            title='RegistryAlreadyExists',
            message=message,
            *args,
            **kwargs
        )